#!/usr/bin/env python3
"""Freeze and validate the digest-bound flat-to-category skill path migration."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any

from skill_registry import RegistryError, SkillRegistry, load_registry
from sync_installed_skills import SyncError, file_hashes, tree_digest


DEFAULT_MANIFEST = Path("migrations/skill-layout-v2.json")
MARKDOWN_LINK_RE = re.compile(r"(?P<prefix>!?\[[^\]\n]*\]\()(?P<body>[^)\n]+)(?P<suffix>\))")


class LayoutMigrationError(RuntimeError):
    """Raised when the path migration cannot be proven safe."""


def _proposal_digest(data: dict[str, Any]) -> str:
    """Bind approval to paths, both byte states, and compatibility invariants."""

    payload = {
        "category_values": data["category_model"]["values"],
        "invariants": data["invariants"],
        "moves": data["moves"],
        "markdown_link_rewrites": data["markdown_link_rewrites"],
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _destination(record: dict[str, Any]) -> str:
    if record["maturity"] == "promoted":
        return f"skills/{record['category']}/{record['name']}"
    root = {
        "incubating": "incubator",
        "misc": "misc",
        "deprecated": "deprecated",
    }[record["maturity"]]
    return f"{root}/{record['name']}"


def _split_link_body(body: str) -> tuple[str, str, bool]:
    """Return the target, untouched title suffix, and angle-bracket style."""

    stripped = body.lstrip()
    leading = body[: len(body) - len(stripped)]
    if stripped.startswith("<"):
        closing = stripped.find(">")
        if closing < 0:
            return body, "", False
        return stripped[1:closing], leading + stripped[closing + 1 :], True
    match = re.match(r"([^\s]+)(.*)\Z", stripped, re.DOTALL)
    if not match:
        return body, "", False
    return match.group(1), leading + match.group(2), False


def _map_path(path: Path, mappings: list[tuple[Path, Path]]) -> Path:
    for source, destination in mappings:
        if path == source or source in path.parents:
            return destination / path.relative_to(source)
    return path


def _relative_target(target: Path, parent: Path) -> str:
    return Path(os.path.relpath(target, parent)).as_posix()


def rewrite_markdown_links(
    text: str,
    *,
    source_file: Path,
    destination_file: Path,
    mappings: list[tuple[Path, Path]],
    repo_root: Path,
) -> tuple[str, list[dict[str, str]]]:
    """Rewrite repository-local Markdown targets for a virtual path move."""

    repo_root = repo_root.resolve()
    rewrites: list[dict[str, str]] = []

    def replace(match: re.Match[str]) -> str:
        body = match.group("body")
        raw_target, suffix, angle_wrapped = _split_link_body(body)
        if (
            not raw_target
            or raw_target.startswith(("#", "/", "http://", "https://", "mailto:", "data:"))
            or "://" in raw_target
        ):
            return match.group(0)
        path_part, anchor = (raw_target.split("#", 1) + [""])[:2]
        if not path_part:
            return match.group(0)
        source_target = (source_file.parent / path_part).resolve()
        if source_target != repo_root and repo_root not in source_target.parents:
            return match.group(0)
        destination_target = _map_path(source_target, mappings)
        rewritten_path = _relative_target(destination_target, destination_file.parent)
        rewritten_target = rewritten_path + (f"#{anchor}" if anchor else "")
        if rewritten_target == raw_target:
            return match.group(0)
        rewrites.append({
            "source_file": source_file.relative_to(repo_root).as_posix(),
            "destination_file": destination_file.relative_to(repo_root).as_posix(),
            "before": raw_target,
            "after": rewritten_target,
        })
        target_text = f"<{rewritten_target}>" if angle_wrapped else rewritten_target
        return f"{match.group('prefix')}{target_text}{suffix}{match.group('suffix')}"

    return MARKDOWN_LINK_RE.sub(replace, text), rewrites


def _transformed_tree(
    repo_root: Path,
    source_relative: str,
    destination_relative: str,
    mappings: list[tuple[Path, Path]],
) -> tuple[dict[str, str], list[dict[str, str]]]:
    source_root = repo_root / PurePosixPath(source_relative)
    destination_root = repo_root / PurePosixPath(destination_relative)
    source_hashes = file_hashes(source_root)
    destination_hashes: dict[str, str] = {}
    rewrites: list[dict[str, str]] = []
    for relative in sorted(source_hashes):
        source_file = source_root / PurePosixPath(relative)
        content = source_file.read_bytes()
        if source_file.suffix == ".md":
            try:
                text = content.decode("utf-8")
            except UnicodeDecodeError as error:
                raise LayoutMigrationError(f"Markdown file is not UTF-8: {source_file}") from error
            transformed, file_rewrites = rewrite_markdown_links(
                text,
                source_file=source_file,
                destination_file=destination_root / PurePosixPath(relative),
                mappings=mappings,
                repo_root=repo_root,
            )
            content = transformed.encode("utf-8")
            rewrites.extend(file_rewrites)
        destination_hashes[relative] = hashlib.sha256(content).hexdigest()
    return destination_hashes, rewrites


def build_manifest(repo_root: Path, registry: SkillRegistry) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    base_moves: list[dict[str, Any]] = []
    for record in registry.records:
        source = record["path"]
        expected_source = f"skills/{record['name']}"
        if source != expected_source:
            raise LayoutMigrationError(
                f"registry skill '{record['name']}' is not at the expected flat pre-migration path {expected_source}"
            )
        destination = _destination(record)
        if (repo_root / PurePosixPath(destination)).exists():
            raise LayoutMigrationError(f"destination already exists: {destination}")
        base_moves.append({
            "name": record["name"],
            "category": record["category"],
            "maturity": record["maturity"],
            "source": source,
            "destination": destination,
            "installed_name": record["name"],
            "output_root": record["output_root"],
        })
    mappings = [
        (repo_root / PurePosixPath(move["source"]), repo_root / PurePosixPath(move["destination"]))
        for move in base_moves
    ]
    moves: list[dict[str, Any]] = []
    all_rewrites: list[dict[str, str]] = []
    for move in base_moves:
        source_hashes = file_hashes(repo_root / PurePosixPath(move["source"]))
        destination_hashes, rewrites = _transformed_tree(
            repo_root, move["source"], move["destination"], mappings
        )
        moves.append({
            **move,
            "source_tree_sha256": tree_digest(source_hashes),
            "source_files": len(source_hashes),
            "destination_tree_sha256": tree_digest(destination_hashes),
            "destination_files": len(destination_hashes),
        })
        all_rewrites.extend(rewrites)
    manifest = {
        "schema_version": 2,
        "migration": "skill-layout-v2",
        "status": "ready" if registry.data["category_model"]["status"] == "approved" else "awaiting-owner-confirmation",
        "category_model": registry.data["category_model"],
        "invariants": {
            "installed_names_unchanged": True,
            "frontmatter_names_unchanged": True,
            "output_roots_unchanged": True,
            "pipeline_slugs_unchanged": True,
        },
        "moves": moves,
        "markdown_link_rewrites": all_rewrites,
    }
    manifest["proposal_sha256"] = _proposal_digest(manifest)
    return manifest


def _validate_rewrite_records(value: Any, errors: list[str]) -> None:
    if not isinstance(value, list):
        errors.append("layout manifest: markdown_link_rewrites must be an array")
        return
    required = {"source_file", "destination_file", "before", "after"}
    for index, record in enumerate(value):
        if not isinstance(record, dict) or set(record) != required:
            errors.append(f"layout manifest rewrite[{index}]: fields do not match schema")
        elif not all(isinstance(item, str) and item for item in record.values()):
            errors.append(f"layout manifest rewrite[{index}]: values must be non-empty strings")


def validate_manifest(repo_root: Path, registry: SkillRegistry, data: Any) -> tuple[str | None, list[str]]:
    repo_root = repo_root.resolve()
    errors: list[str] = []
    if not isinstance(data, dict):
        return None, ["layout manifest: expected an object"]
    expected_fields = {
        "schema_version",
        "migration",
        "status",
        "category_model",
        "invariants",
        "moves",
        "markdown_link_rewrites",
        "proposal_sha256",
    }
    if set(data) != expected_fields:
        errors.append("layout manifest: fields do not match schema")
        return None, errors
    if data["schema_version"] != 2 or data["migration"] != "skill-layout-v2":
        errors.append("layout manifest: identity mismatch")
    expected_digest = _proposal_digest(data)
    if data["proposal_sha256"] != expected_digest:
        errors.append("layout manifest: proposal digest mismatch")
    if data["status"] not in {"awaiting-owner-confirmation", "ready", "completed"}:
        errors.append("layout manifest: invalid status")
    if data["category_model"] != registry.data["category_model"]:
        errors.append("layout manifest: category model disagrees with registry")
    approved = registry.data["category_model"]["status"] == "approved"
    allowed_statuses = {"ready", "completed"} if approved else {"awaiting-owner-confirmation"}
    if data["status"] not in allowed_statuses:
        errors.append("layout manifest: status disagrees with registry approval state")
    invariants = data["invariants"]
    expected_invariants = {
        "installed_names_unchanged",
        "frontmatter_names_unchanged",
        "output_roots_unchanged",
        "pipeline_slugs_unchanged",
    }
    if (
        not isinstance(invariants, dict)
        or set(invariants) != expected_invariants
        or not all(value is True for value in invariants.values())
    ):
        errors.append("layout manifest: compatibility invariants must all be true")
    _validate_rewrite_records(data["markdown_link_rewrites"], errors)
    moves = data["moves"]
    if not isinstance(moves, list):
        return None, errors + ["layout manifest: moves must be an array"]
    if [move.get("name") for move in moves if isinstance(move, dict)] != sorted(registry.names):
        errors.append("layout manifest: move names do not exactly match the registry")
    by_name = registry.by_name
    states: set[str] = set()
    destinations: set[str] = set()
    fields = {
        "name",
        "category",
        "maturity",
        "source",
        "destination",
        "installed_name",
        "output_root",
        "source_tree_sha256",
        "source_files",
        "destination_tree_sha256",
        "destination_files",
    }
    for index, move in enumerate(moves):
        location = f"layout manifest move[{index}]"
        if not isinstance(move, dict) or set(move) != fields:
            errors.append(f"{location}: fields do not match schema")
            continue
        name = move["name"]
        record = by_name.get(name)
        if record is None:
            errors.append(f"{location}: unknown skill '{name}'")
            continue
        expected_source = f"skills/{name}"
        expected_destination = _destination(record)
        if move["source"] != expected_source or move["destination"] != expected_destination:
            errors.append(f"{location}: path mapping disagrees with registry category")
        if move["destination"] in destinations:
            errors.append(f"{location}: duplicate destination")
        destinations.add(move["destination"])
        if (
            move["category"] != record["category"]
            or move["maturity"] != record["maturity"]
            or move["installed_name"] != name
            or move["output_root"] != record["output_root"]
        ):
            errors.append(f"{location}: public compatibility metadata drift")
        source_path = repo_root / PurePosixPath(move["source"])
        destination_path = repo_root / PurePosixPath(move["destination"])
        if source_path.is_dir() and not destination_path.exists():
            state = "pre-move"
            active_path = source_path
            expected_tree = move["source_tree_sha256"]
            expected_files = move["source_files"]
        elif destination_path.is_dir() and not source_path.exists():
            state = "post-move"
            active_path = destination_path
            expected_tree = move["destination_tree_sha256"]
            expected_files = move["destination_files"]
        else:
            errors.append(f"{location}: expected exactly one of source or destination to exist")
            continue
        states.add(state)
        if record["path"] != active_path.relative_to(repo_root).as_posix():
            errors.append(f"{location}: registry path does not match active path")
        if data["status"] != "completed":
            hashes = file_hashes(active_path)
            if tree_digest(hashes) != expected_tree or len(hashes) != expected_files:
                errors.append(f"{location}: active tree digest or file count changed")
    if len(states) > 1:
        errors.append("layout manifest: mixed pre-move and post-move state")
    state = next(iter(states), None)
    if state == "post-move" and registry.data["category_model"]["status"] != "approved":
        errors.append("layout manifest: post-move state requires recorded owner approval")
    if data["status"] == "completed" and state != "post-move":
        errors.append("layout manifest: completed status requires post-move state")
    if state == "pre-move" and not errors:
        try:
            rebuilt = build_manifest(repo_root, registry)
        except (LayoutMigrationError, SyncError) as error:
            errors.append(f"layout manifest: cannot reproduce proposal: {error}")
        else:
            if rebuilt["moves"] != data["moves"] or rebuilt["markdown_link_rewrites"] != data["markdown_link_rewrites"]:
                errors.append("layout manifest: destination simulation or link rewrites changed")
    return state, errors


def write_manifest(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temporary.replace(path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--write", action="store_true", help="Write the pre-migration manifest atomically.")
    parser.add_argument("--check", action="store_true", help="Validate the committed manifest (default).")
    args = parser.parse_args(argv)
    if args.write and args.check:
        parser.error("choose --write or --check")
    repo_root = args.repo_root.resolve()
    manifest_path = (args.manifest or repo_root / DEFAULT_MANIFEST).resolve()
    try:
        registry = load_registry(repo_root)
        if args.write:
            data = build_manifest(repo_root, registry)
            write_manifest(manifest_path, data)
        else:
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
        state, errors = validate_manifest(repo_root, registry, data)
    except (OSError, json.JSONDecodeError, RegistryError, LayoutMigrationError, SyncError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Layout migration validation failed: {len(errors)} error(s).", file=sys.stderr)
        return 1
    action = "Wrote and validated" if args.write else "Validated"
    print(
        f"{action} {len(data['moves'])} digest-bound layout moves in {state} state; "
        f"{len(data['markdown_link_rewrites'])} Markdown link rewrite(s); "
        f"proposal sha256 {data['proposal_sha256']}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
