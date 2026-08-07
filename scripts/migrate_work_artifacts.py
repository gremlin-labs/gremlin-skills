#!/usr/bin/env python3
"""Safely migrate legacy Gremlin work roots into agent-work/{slug}/{skill}/."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


ROOT_SKILLS = {
    "brainstorms": "brainstormpro",
    "feature-specs": "feature-clone",
    "migrations": "migratepro",
    "proposals": "audit-plan",
    "restructures": "restructure",
    "tests": "testpro",
}
LEGACY_ROOTS = sorted(set(ROOT_SKILLS) | {"plans", "goals", "audits", "releases"})


class MigrationError(RuntimeError):
    """Raised when a migration cannot complete or recover safely."""


@dataclass(frozen=True)
class Move:
    source: str
    destination: str
    skill: str
    slug: str
    source_tree_sha256: str


def tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            raise MigrationError(f"symbolic links are not supported: {path}")
        if path.is_file():
            payload = path.read_bytes()
            digest.update(relative.encode("utf-8"))
            digest.update(b"\0")
            digest.update(hashlib.sha256(payload).digest())
    return digest.hexdigest()


def _classify(root: str, artifact: Path) -> str:
    names = {path.name for path in artifact.rglob("*") if path.is_file()}
    if root == "plans":
        if {"DESIGN-AUDIT.md", "TOKEN-INVENTORY.md"} & names:
            return "designpro"
        if {"WORKSPACE-AUDIT.md", "REPO-INVENTORY.md"} & names:
            return "workspacepro"
        return "planpro"
    if root == "goals":
        return "feature-goal" if "spec-link.md" in names else "goalpro"
    if root == "audits":
        return "stripe-audit" if {"INVARIANTS.md", "EVENT-MATRIX.md"} & names else "audit-compare"
    if root == "releases":
        return "releasepro"
    return ROOT_SKILLS[root]


def _release_slug(name: str) -> str:
    normalized = name.lower().removeprefix("v")
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized).strip("-")
    if not normalized:
        raise MigrationError(f"release directory has no usable version: {name!r}")
    return f"release-v{normalized}"


def discover(repo: Path) -> tuple[list[Move], list[str]]:
    repo = repo.resolve()
    moves: list[Move] = []
    errors: list[str] = []
    for root_name in LEGACY_ROOTS:
        legacy = repo / root_name
        if not legacy.exists():
            continue
        if not legacy.is_dir():
            errors.append(f"legacy root is not a directory: {legacy}")
            continue
        for artifact in sorted(legacy.iterdir()):
            if not artifact.is_dir() or artifact.is_symlink():
                errors.append(f"unclassified file at legacy root: {artifact}")
                continue
            try:
                skill = _classify(root_name, artifact)
                slug = _release_slug(artifact.name) if root_name == "releases" else artifact.name
                destination = repo / "agent-work" / slug / skill
                if destination.exists() or destination.is_symlink():
                    errors.append(f"destination collision: {destination}")
                    continue
                moves.append(Move(str(artifact), str(destination), skill, slug, tree_digest(artifact)))
            except (OSError, MigrationError) as error:
                errors.append(str(error))
    return moves, errors


def _write_json_atomic(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def _write_text_atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(text, encoding="utf-8")
    os.replace(temporary, path)


def _updated_index(index: Path, slug: str, migrated: list[Move]) -> str:
    if index.exists():
        text = index.read_text(encoding="utf-8").rstrip() + "\n"
    else:
        text = (
            f"# Work: {slug}\n\n"
            "## Outcome\n\nMigrated legacy Gremlin work artifacts.\n\n"
            "## Ownership\n\n- Migration owner: `migrate_work_artifacts.py`\n\n"
            "## Status\n\n`ACTIVE` — migrated state requires owner review.\n\n"
            "## Stages\n\n| Skill | Status | Primary artifact | Approval |\n"
            "|---|---|---|---|\n\n"
            "## Current handoff\n\nReview migrated state before resuming execution.\n\n"
            "## Decisions and material deltas\n\n"
            "## Final evidence\n"
        )
    heading = "## Migration history"
    if heading not in text:
        text = text.rstrip() + f"\n\n{heading}\n"
    for move in migrated:
        source = Path(move.source).as_posix()
        entry = f"- Migrated `{source}` into `{move.skill}/` with source tree SHA-256 `{move.source_tree_sha256}`."
        if entry not in text:
            text = text.rstrip() + f"\n{entry}\n"
    return text


def _preflight(repo: Path, moves: list[Move], journal_path: Path) -> None:
    repo = repo.resolve()
    if not journal_path.resolve().is_relative_to(repo):
        raise MigrationError("journal path must be inside the repository")
    sources: list[Path] = []
    destinations: list[Path] = []
    for move in moves:
        source = Path(move.source).resolve()
        destination = Path(move.destination).resolve()
        if source == repo or destination == repo or not source.is_relative_to(repo) or not destination.is_relative_to(repo):
            raise MigrationError(f"migration path escapes repository: {source} -> {destination}")
        if source.is_symlink() or not source.is_dir():
            raise MigrationError(f"source is not a real directory: {source}")
        if destination.exists() or destination.is_symlink():
            raise MigrationError(f"destination collision: {destination}")
        if tree_digest(source) != move.source_tree_sha256:
            raise MigrationError(f"source changed after discovery: {source}")
        sources.append(source)
        destinations.append(destination)
    all_paths = sources + destinations
    if len(set(all_paths)) != len(all_paths):
        raise MigrationError("duplicate resolved source or destination")
    for index, path in enumerate(all_paths):
        for other in all_paths[index + 1:]:
            if path in other.parents or other in path.parents:
                raise MigrationError(f"overlapping migration paths: {path} and {other}")


def apply_moves(repo: Path, moves: list[Move], journal_path: Path | None = None) -> None:
    repo = repo.resolve()
    journal_path = (journal_path or repo / "agent-work" / "migrate-legacy-work-artifacts" / "goalpro" / "MIGRATION-JOURNAL.json").resolve()
    _preflight(repo, moves, journal_path)
    by_slug: dict[str, list[Move]] = {}
    for move in moves:
        by_slug.setdefault(move.slug, []).append(move)
    index_backups: dict[str, str | None] = {}
    for slug in by_slug:
        index = repo / "agent-work" / slug / "WORK.md"
        index_backups[str(index)] = index.read_text(encoding="utf-8") if index.exists() else None
    journal: dict[str, Any] = {
        "schema_version": 1,
        "state": "applying",
        "repository": str(repo),
        "moves": [{**asdict(move), "status": "pending"} for move in moves],
        "index_backups": index_backups,
    }
    if journal_path.exists():
        raise MigrationError(f"journal already exists: {journal_path}")
    _write_json_atomic(journal_path, journal)
    completed: list[Move] = []
    try:
        for index, move in enumerate(moves):
            source = Path(move.source)
            destination = Path(move.destination)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source), str(destination))
            if tree_digest(destination) != move.source_tree_sha256:
                raise MigrationError(f"post-move digest mismatch: {destination}")
            completed.append(move)
            journal["moves"][index]["status"] = "moved"
            _write_json_atomic(journal_path, journal)
        for slug, slug_moves in by_slug.items():
            index = repo / "agent-work" / slug / "WORK.md"
            _write_text_atomic(index, _updated_index(index, slug, slug_moves))
        for root_name in LEGACY_ROOTS:
            path = repo / root_name
            if path.is_dir() and not any(path.iterdir()):
                path.rmdir()
        journal["state"] = "completed"
        _write_json_atomic(journal_path, journal)
    except Exception as error:
        rollback_errors: list[str] = []
        for move in reversed(completed):
            source = Path(move.source)
            destination = Path(move.destination)
            try:
                if source.exists() or not destination.is_dir() or tree_digest(destination) != move.source_tree_sha256:
                    raise MigrationError(f"cannot safely restore {destination}")
                source.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(destination), str(source))
            except Exception as rollback_error:
                rollback_errors.append(str(rollback_error))
        for raw_path, original in index_backups.items():
            index = Path(raw_path)
            try:
                if original is None:
                    index.unlink(missing_ok=True)
                else:
                    _write_text_atomic(index, original)
            except OSError as rollback_error:
                rollback_errors.append(str(rollback_error))
        journal["state"] = "recovery-required" if rollback_errors else "rolled-back"
        journal["error"] = str(error)
        journal["rollback_errors"] = rollback_errors
        _write_json_atomic(journal_path, journal)
        detail = f"; rollback errors: {'; '.join(rollback_errors)}" if rollback_errors else ""
        raise MigrationError(f"migration failed and {journal['state']}: {error}{detail}") from error


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--apply", action="store_true", help="perform moves; default is dry-run")
    parser.add_argument("--journal", type=Path, help="recovery journal path inside the repository")
    parser.add_argument("--json", action="store_true", help="emit a machine-readable report")
    args = parser.parse_args(argv)
    repo = args.repo_root.resolve()
    moves, errors = discover(repo)
    report = {
        "mode": "apply" if args.apply else "dry-run",
        "moves": [asdict(move) for move in moves],
        "errors": errors,
    }
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"{report['mode']}: {len(moves)} move(s), {len(errors)} error(s)")
        for move in moves:
            print(f"MOVE {move.source} -> {move.destination} sha256:{move.source_tree_sha256}")
        for error in errors:
            print(f"ERROR {error}", file=sys.stderr)
    if errors:
        return 2
    if args.apply:
        try:
            journal = args.journal.resolve() if args.journal else None
            apply_moves(repo, moves, journal_path=journal)
        except MigrationError as error:
            print(f"ERROR {error}", file=sys.stderr)
            return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
