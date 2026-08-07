#!/usr/bin/env python3
"""Produce a read-only candidate inventory of Git repositories in a workspace."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlsplit, urlunsplit


DEFAULT_EXCLUDES = {
    ".cache", ".git", ".next", ".venv", ".zig-cache", "artifacts", "build",
    "coverage", "dist", "models", "node_modules", "out", "target", "vendor", "zig-out",
}
TOOLCHAIN_FILES = (
    "package.json", "pyproject.toml", "Cargo.toml", "go.mod", "build.zig",
    "build.zig.zon", "Package.swift", "Gemfile", "pom.xml", "build.gradle",
    "Makefile", "justfile", "Taskfile.yml", "mise.toml",
)
DOC_FILES = ("README.md", "AGENTS.md", "CLAUDE.md", "CONTRIBUTING.md", "CONTEXT.md", "ARCHITECTURE.md")


def run_git(path: Path, *args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", "-C", str(path), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result.stdout.strip() if result.returncode == 0 else ""


def sanitize_remote(raw: str) -> str:
    value = raw.strip()
    if not value:
        return value
    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", value):
        parts = urlsplit(value)
        host = parts.hostname or ""
        if ":" in host and not host.startswith("["):
            host = f"[{host}]"
        if parts.port:
            host = f"{host}:{parts.port}"
        return urlunsplit((parts.scheme, host, parts.path, "", ""))
    without_secrets = value.split("@", 1)[1] if "@" in value else value
    return re.split(r"[?#]", without_secrets, maxsplit=1)[0]


def candidates(root: Path, max_depth: int, excludes: set[str]) -> Iterable[Path]:
    root = root.resolve()
    if (root / ".git").exists() or run_git(root, "rev-parse", "--is-inside-work-tree", check=False) == "true":
        yield root
    if not root.is_dir():
        return
    for current, dirs, _files in os.walk(root):
        path = Path(current)
        depth = len(path.relative_to(root).parts)
        dirs[:] = [name for name in dirs if name not in excludes and not name.startswith(".worktrees")]
        if depth >= max_depth:
            dirs[:] = []
        if path != root and (path / ".git").exists():
            yield path
            dirs[:] = []


def _resolved_git_path(repo: Path, raw: str) -> Path:
    path = Path(raw)
    return path.resolve() if path.is_absolute() else (repo / path).resolve()


def inspect_repo(path: Path, workspace_root: Path) -> dict[str, Any]:
    top = Path(run_git(path, "rev-parse", "--show-toplevel")).resolve()
    git_dir = _resolved_git_path(top, run_git(top, "rev-parse", "--git-dir"))
    common_dir = _resolved_git_path(top, run_git(top, "rev-parse", "--git-common-dir"))
    superproject = run_git(top, "rev-parse", "--show-superproject-working-tree", check=False)
    form = "submodule" if superproject else "linked-worktree" if git_dir != common_dir else "main-worktree"
    branch = run_git(top, "symbolic-ref", "--short", "-q", "HEAD", check=False) or "detached"
    commit = run_git(top, "rev-parse", "HEAD")
    status = run_git(top, "status", "--porcelain=v1", "--untracked-files=normal", check=False).splitlines()
    tracked_dirty = sum(not line.startswith("??") for line in status)
    untracked = sum(line.startswith("??") for line in status)
    upstream = run_git(top, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}", check=False)
    ahead = behind = None
    if upstream:
        counts = run_git(top, "rev-list", "--left-right", "--count", f"HEAD...{upstream}", check=False).split()
        if len(counts) == 2:
            ahead, behind = map(int, counts)
    remotes: dict[str, str] = {}
    for name in run_git(top, "remote", check=False).splitlines():
        remotes[name] = sanitize_remote(run_git(top, "remote", "get-url", name, check=False))
    try:
        relative = top.relative_to(workspace_root).as_posix()
    except ValueError:
        relative = top.as_posix()

    def display(local_path: Path) -> str:
        try:
            return local_path.relative_to(workspace_root).as_posix()
        except ValueError:
            return f"external:{local_path.name}"

    return {
        "name": top.name,
        "path": relative or ".",
        "git_form": form,
        "git_top_level": display(top),
        "git_common_dir": display(common_dir),
        "superproject": display(Path(superproject).resolve()) if superproject else None,
        "branch": branch,
        "commit": commit,
        "dirty": {"tracked": tracked_dirty, "untracked": untracked},
        "upstream": upstream or None,
        "ahead": ahead,
        "behind": behind,
        "remotes": remotes,
        "toolchain_files": [name for name in TOOLCHAIN_FILES if (top / name).is_file()],
        "documentation": [name for name in DOC_FILES if (top / name).is_file()],
    }


def inventory(roots: list[Path], max_depth: int = 3, excludes: set[str] | None = None) -> dict[str, Any]:
    excludes = DEFAULT_EXCLUDES | (excludes or set())
    workspace_root = Path(os.path.commonpath([str(root.resolve()) for root in roots]))
    seen: set[Path] = set()
    repos: list[dict[str, Any]] = []
    errors: list[str] = []
    for root in roots:
        for candidate in candidates(root, max_depth, excludes):
            try:
                top = Path(run_git(candidate, "rev-parse", "--show-toplevel")).resolve()
                if top in seen:
                    continue
                seen.add(top)
                repos.append(inspect_repo(top, workspace_root))
            except (OSError, RuntimeError, subprocess.SubprocessError) as error:
                errors.append(f"{candidate}: {error}")
    repos.sort(key=lambda item: item["path"])
    return {
        "version": 1,
        "disclaimer": "Candidate evidence only; verify ownership, role, dependencies, and policy manually.",
        "workspace_root": workspace_root.as_posix(),
        "repositories": repos,
        "errors": errors,
        "summary": {"repositories": len(repos), "errors": len(errors)},
    }


def markdown(report: dict[str, Any]) -> str:
    lines = ["# Workspace inventory", "", f'> {report["disclaimer"]}', "", "| Path | Git form | Branch | Commit | Dirty | Toolchains | Docs |", "|---|---|---|---|---:|---|---|"]
    for repo in report["repositories"]:
        dirty = repo["dirty"]["tracked"] + repo["dirty"]["untracked"]
        lines.append(f'| `{repo["path"]}` | {repo["git_form"]} | `{repo["branch"]}` | `{repo["commit"][:10]}` | {dirty} | {", ".join(repo["toolchain_files"])} | {", ".join(repo["documentation"])} |')
    lines.extend(["", f'Repositories: {report["summary"]["repositories"]}; errors: {report["summary"]["errors"]}.', ""])
    if report["errors"]:
        lines.extend(["## Errors", ""] + [f"- {item}" for item in report["errors"]] + [""])
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("roots", nargs="+", type=Path)
    parser.add_argument("--max-depth", type=int, default=3)
    parser.add_argument("--exclude", action="append", default=[])
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    missing = [str(path) for path in args.roots if not path.exists()]
    if missing or args.max_depth < 0:
        print(f'workspace_inventory: invalid input: {", ".join(missing) if missing else "negative max depth"}', file=sys.stderr)
        return 2
    report = inventory(args.roots, args.max_depth, set(args.exclude))
    rendered = json.dumps(report, indent=2) + "\n" if args.format == "json" else markdown(report)
    try:
        args.output.write_text(rendered, encoding="utf-8") if args.output else sys.stdout.write(rendered)
    except OSError as error:
        print(f"workspace_inventory: {error}", file=sys.stderr)
        return 2
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
