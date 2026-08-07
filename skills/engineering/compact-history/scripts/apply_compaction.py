#!/usr/bin/env python3
"""Preflight, apply, or roll back digest-confirmed compact-history moves."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

from inventory_history import tree_digest
from validate_manifest import canonical_digest, validate


def _contained(root: Path, path: Path) -> bool:
    return path != root and path.is_relative_to(root)


def _write_json_atomic(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def _journal_path(root: Path, run_id: str) -> Path:
    return root / "• compact-history" / "runs" / run_id / "recovery-journal.json"


def _preflight(data: dict[str, Any]) -> tuple[Path, list[dict[str, Any]]]:
    root = Path(data["agent_work_root"]).resolve()
    if not root.is_dir():
        raise ValueError(f"agent_work_root is not a directory: {root}")
    moves: list[dict[str, Any]] = []
    sources: list[Path] = []
    destinations: list[Path] = []
    for operation in data["operations"]:
        if operation["kind"] != "move_tree":
            continue
        source = (root / operation["source"]).resolve()
        destination = (root / operation["destination"]).resolve()
        if not _contained(root, source) or not _contained(root, destination):
            raise ValueError(f"path escapes agent_work_root: {source} -> {destination}")
        if source.is_symlink() or not source.is_dir():
            raise ValueError(f"source is not a real directory: {source}")
        if destination.exists() or destination.is_symlink():
            raise ValueError(f"destination already exists: {destination}")
        actual, _ = tree_digest(source)
        if actual != operation["source_tree_sha256"]:
            raise ValueError(f"source changed: {source}")
        sources.append(source)
        destinations.append(destination)
        moves.append({
            "id": operation["id"],
            "source": str(source),
            "destination": str(destination),
            "source_tree_sha256": actual,
            "status": "pending",
        })
    all_paths = sources + destinations
    if len(set(all_paths)) != len(all_paths):
        raise ValueError("duplicate source or destination after path resolution")
    for index, path in enumerate(all_paths):
        for other in all_paths[index + 1:]:
            if path in other.parents or other in path.parents:
                raise ValueError(f"overlapping move paths are unsafe: {path} and {other}")
    return root, moves


def _rollback(journal_path: Path, expected_digest: str) -> int:
    try:
        journal = json.loads(journal_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(f"cannot read recovery journal: {error}", file=sys.stderr)
        return 2
    if journal.get("manifest_digest") != expected_digest:
        print("recovery journal does not match the confirmed manifest", file=sys.stderr)
        return 2
    try:
        for move in reversed(journal.get("moves", [])):
            if move.get("status") != "moved":
                continue
            source = Path(move["source"])
            destination = Path(move["destination"])
            if source.exists() or not destination.is_dir():
                raise ValueError(f"cannot safely roll back {destination} -> {source}")
            actual, _ = tree_digest(destination)
            if actual != move["source_tree_sha256"]:
                raise ValueError(f"archived tree changed: {destination}")
            source.parent.mkdir(parents=True, exist_ok=True)
            os.replace(destination, source)
            move["status"] = "rolled-back"
            _write_json_atomic(journal_path, journal)
        journal["state"] = "rolled-back"
        _write_json_atomic(journal_path, journal)
        print(f"rolled back compact-history run {journal.get('run_id')}")
        return 0
    except (OSError, ValueError) as error:
        journal["state"] = "recovery-required"
        journal["error"] = str(error)
        _write_json_atomic(journal_path, journal)
        print(f"rollback stopped: {error}", file=sys.stderr)
        return 3


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--confirm", required=True, help="exact manifest SHA-256, with optional sha256: prefix")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--apply", action="store_true")
    mode.add_argument("--rollback", action="store_true")
    args = parser.parse_args()
    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(f"cannot read manifest: {error}", file=sys.stderr)
        return 2
    errors = validate(data)
    digest = canonical_digest(data) if isinstance(data, dict) else ""
    if errors or args.confirm not in {digest, f"sha256:{digest}"}:
        print("manifest invalid or confirmation digest mismatch", file=sys.stderr)
        return 2
    if args.rollback:
        root = Path(data["agent_work_root"]).resolve()
        if not root.is_dir():
            print(f"agent_work_root is not a directory: {root}", file=sys.stderr)
            return 2
        journal_path = _journal_path(root, data["run_id"])
        return _rollback(journal_path, digest)
    try:
        root, moves = _preflight(data)
    except (OSError, ValueError) as error:
        print(f"preflight failed: {error}", file=sys.stderr)
        return 2
    journal_path = _journal_path(root, data["run_id"])
    print(f"{'apply' if args.apply else 'dry-run'}: {len(moves)} move(s), digest sha256:{digest}")
    if not args.apply:
        return 0
    if journal_path.exists():
        print(f"recovery journal already exists: {journal_path}", file=sys.stderr)
        return 2
    journal: dict[str, Any] = {
        "schema_version": 1,
        "run_id": data["run_id"],
        "manifest_digest": digest,
        "state": "applying",
        "moves": moves,
    }
    _write_json_atomic(journal_path, journal)
    try:
        for move in moves:
            source = Path(move["source"])
            destination = Path(move["destination"])
            destination.parent.mkdir(parents=True, exist_ok=True)
            os.replace(source, destination)
            move["status"] = "moved"
            _write_json_atomic(journal_path, journal)
            actual, _ = tree_digest(destination)
            if actual != move["source_tree_sha256"]:
                raise ValueError(f"post-move digest mismatch: {destination}")
        journal["state"] = "completed"
        _write_json_atomic(journal_path, journal)
        print(f"completed compact-history run; recovery journal: {journal_path}")
        return 0
    except (OSError, ValueError) as error:
        journal["state"] = "recovery-required"
        journal["error"] = str(error)
        _write_json_atomic(journal_path, journal)
        print(f"apply stopped; use --rollback after inspection: {error}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
