#!/usr/bin/env python3
"""Validate Workspacepro JSON manifest and optional generated lock state."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any


ROLES = {"app", "service", "library", "tool", "experiment", "reference", "vendor"}
LIFECYCLES = {"active", "optional", "incubating", "deprecated", "archived", "local-only", "planned"}
DEPENDENCY_KINDS = {"build", "runtime", "development", "integration-test", "documentation", "reference", "process", "package", "local-override"}
COMMIT_RE = re.compile(r"^[0-9a-fA-F]{40}(?:[0-9a-fA-F]{24})?$")


class ManifestInputError(ValueError):
    """Raised for malformed top-level input."""


def canonical_digest(manifest: dict[str, Any]) -> str:
    payload = json.dumps(manifest, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def _portable_path(raw: Any) -> bool:
    if not isinstance(raw, str) or not raw or "\\" in raw:
        return False
    path = PurePosixPath(raw)
    return not path.is_absolute() and ".." not in path.parts and str(path) not in {".", ""}


def _cycle(graph: dict[str, list[str]]) -> list[str] | None:
    visiting: list[str] = []
    visited: set[str] = set()

    def walk(node: str) -> list[str] | None:
        if node in visiting:
            index = visiting.index(node)
            return visiting[index:] + [node]
        if node in visited:
            return None
        visiting.append(node)
        for dependency in graph.get(node, []):
            result = walk(dependency)
            if result:
                return result
        visiting.pop()
        visited.add(node)
        return None

    for node in graph:
        result = walk(node)
        if result:
            return result
    return None


def validate(manifest: dict[str, Any], lock: dict[str, Any] | None = None, root: Path | None = None) -> dict[str, Any]:
    issues: list[dict[str, str]] = []

    def issue(code: str, location: str, message: str) -> None:
        issues.append({"code": code, "location": location, "message": message})

    if not isinstance(manifest, dict):
        raise ManifestInputError("manifest must be an object")
    if not isinstance(manifest.get("version"), int) or manifest["version"] < 1:
        issue("MANIFEST_VERSION", "version", "version must be a positive integer")
    workspace = manifest.get("workspace")
    if not isinstance(workspace, dict) or not isinstance(workspace.get("name"), str) or not workspace["name"].strip():
        issue("WORKSPACE_NAME", "workspace.name", "workspace needs a non-empty name")
    projects = manifest.get("projects")
    if not isinstance(projects, list):
        raise ManifestInputError("projects must be an array")

    names: set[str] = set()
    paths: set[str] = set()
    graph: dict[str, list[str]] = {}
    project_by_name: dict[str, dict[str, Any]] = {}
    for index, project in enumerate(projects):
        location = f"projects[{index}]"
        if not isinstance(project, dict):
            issue("PROJECT_OBJECT", location, "project must be an object")
            continue
        name = project.get("name")
        path = project.get("path")
        if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            issue("PROJECT_NAME", f"{location}.name", "name must be non-empty kebab-case")
            continue
        if name in names:
            issue("DUPLICATE_NAME", f"{location}.name", f"duplicate project name {name!r}")
        names.add(name)
        project_by_name[name] = project
        if not _portable_path(path):
            issue("PROJECT_PATH", f"{location}.path", "path must be portable, relative, and contained")
        elif path in paths:
            issue("DUPLICATE_PATH", f"{location}.path", f"duplicate project path {path!r}")
        else:
            paths.add(path)
            if root is not None:
                resolved_root = root.resolve()
                resolved_path = (resolved_root / path).resolve()
                if not resolved_path.is_relative_to(resolved_root):
                    issue("PATH_ESCAPE", f"{location}.path", "resolved path escapes the workspace root")
                elif not resolved_path.exists() and project.get("lifecycle") not in {"planned", "archived"}:
                    issue("MISSING_PATH", f"{location}.path", f"registered path does not exist: {path}")
        if project.get("role") not in ROLES:
            issue("PROJECT_ROLE", f"{location}.role", f"role must be one of {', '.join(sorted(ROLES))}")
        if project.get("lifecycle") not in LIFECYCLES:
            issue("PROJECT_LIFECYCLE", f"{location}.lifecycle", f"lifecycle must be one of {', '.join(sorted(LIFECYCLES))}")
        groups = project.get("groups", [])
        if not isinstance(groups, list) or not all(isinstance(item, str) and item for item in groups) or len(groups) != len(set(groups)):
            issue("PROJECT_GROUPS", f"{location}.groups", "groups must be unique non-empty strings")
        dependencies = project.get("dependencies", [])
        graph[name] = []
        if not isinstance(dependencies, list):
            issue("DEPENDENCIES", f"{location}.dependencies", "dependencies must be an array")
            continue
        for dep_index, dependency in enumerate(dependencies):
            dep_location = f"{location}.dependencies[{dep_index}]"
            if not isinstance(dependency, dict) or not isinstance(dependency.get("project"), str):
                issue("DEPENDENCY_OBJECT", dep_location, "dependency needs a project name")
                continue
            target = dependency["project"]
            graph[name].append(target)
            if target == name:
                issue("SELF_DEPENDENCY", dep_location, "project cannot depend on itself")
            if dependency.get("kind") not in DEPENDENCY_KINDS:
                issue("DEPENDENCY_KIND", f"{dep_location}.kind", f"unknown dependency kind {dependency.get('kind')!r}")

    for source, targets in graph.items():
        for target in targets:
            if target not in names:
                issue("UNKNOWN_DEPENDENCY", f"projects.{source}.dependencies", f"unknown project {target!r}")
                continue
            source_role = project_by_name[source].get("role")
            target_role = project_by_name[target].get("role")
            if source_role not in {"reference", "vendor"} and target_role == "reference":
                kinds = [dep.get("kind") for dep in project_by_name[source].get("dependencies", []) if dep.get("project") == target]
                if any(kind not in {"documentation", "reference"} for kind in kinds):
                    issue("EDITABLE_REFERENCE_DEPENDENCY", f"projects.{source}.dependencies", "owned project cannot use a reference as an editable code dependency")
    cycle = _cycle(graph)
    if cycle:
        issue("DEPENDENCY_CYCLE", "projects", "dependency cycle: " + " -> ".join(cycle))

    shared_paths = manifest.get("shared_paths", [])
    if not isinstance(shared_paths, list):
        issue("SHARED_PATHS", "shared_paths", "shared_paths must be an array")
    else:
        for index, item in enumerate(shared_paths):
            if not isinstance(item, dict) or not _portable_path(item.get("path")):
                issue("SHARED_PATH", f"shared_paths[{index}]", "shared path must be an object with a portable relative path")

    if lock is not None:
        if not isinstance(lock, dict):
            raise ManifestInputError("lock must be an object")
        expected_digest = canonical_digest(manifest)
        if lock.get("manifest_digest") != expected_digest:
            issue("LOCK_DIGEST", "lock.manifest_digest", f"expected {expected_digest}")
        locked = lock.get("projects")
        if not isinstance(locked, dict):
            issue("LOCK_PROJECTS", "lock.projects", "lock projects must be an object keyed by project name")
            locked = {}
        required = {name for name, project in project_by_name.items() if project.get("lifecycle") not in {"planned", "local-only", "archived"}}
        for name in sorted(required - set(locked)):
            issue("MISSING_LOCK", f"lock.projects.{name}", "required project is not locked")
        for name in sorted(set(locked) - names):
            issue("STALE_LOCK", f"lock.projects.{name}", "lock contains an unknown project")
        for name, item in locked.items():
            commit = item.get("commit") if isinstance(item, dict) else None
            if name in names and (not isinstance(commit, str) or not COMMIT_RE.fullmatch(commit)):
                issue("LOCK_COMMIT", f"lock.projects.{name}.commit", "commit must be a full 40- or 64-character hexadecimal object ID")

    issues.sort(key=lambda item: (item["location"], item["code"]))
    return {"version": 1, "valid": not issues, "manifest_digest": canonical_digest(manifest), "issues": issues, "summary": {"projects": len(projects), "issues": len(issues)}}


def markdown(report: dict[str, Any]) -> str:
    lines = ["# Workspace manifest validation", "", f'Valid: {"yes" if report["valid"] else "no"}', "", f'Manifest digest: `{report["manifest_digest"]}`', ""]
    if report["issues"]:
        lines.extend(["| Code | Location | Message |", "|---|---|---|"])
        for item in report["issues"]:
            lines.append(f'| {item["code"]} | `{item["location"]}` | {item["message"]} |')
        lines.append("")
    lines.append(f'Projects: {report["summary"]["projects"]}; issues: {report["summary"]["issues"]}.')
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--lock", type=Path)
    parser.add_argument("--root", type=Path, help="optionally verify registered paths")
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        lock = json.loads(args.lock.read_text(encoding="utf-8")) if args.lock else None
        report = validate(manifest, lock, args.root.resolve() if args.root else None)
        rendered = json.dumps(report, indent=2) + "\n" if args.format == "json" else markdown(report)
        args.output.write_text(rendered, encoding="utf-8") if args.output else sys.stdout.write(rendered)
        return 0 if report["valid"] else 1
    except (OSError, json.JSONDecodeError, ManifestInputError) as error:
        print(f"validate_workspace_manifest: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
