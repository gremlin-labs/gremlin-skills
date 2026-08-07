#!/usr/bin/env python3
"""Validate a compact-history archive manifest and its confirmation digest."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any


DIGEST_RE = re.compile(r"^[0-9a-f]{64}$")
RUN_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
ARCHIVE_PREFIX = PurePosixPath("• compact-history/archive")


def canonical_digest(data: dict[str, Any]) -> str:
    clean = dict(data)
    clean.pop("confirmation_sha256", None)
    payload = json.dumps(
        clean,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _safe_relative(value: Any) -> bool:
    if not isinstance(value, str) or not value or "\\" in value:
        return False
    path = PurePosixPath(value)
    return not path.is_absolute() and ".." not in path.parts and str(path) not in {"", "."}


def validate(data: Any) -> list[str]:
    if not isinstance(data, dict):
        return ["manifest must be an object"]

    errors: list[str] = []
    if data.get("schema_version") != 1:
        errors.append("schema_version must equal 1")
    run_id = data.get("run_id")
    if not isinstance(run_id, str) or not RUN_ID_RE.fullmatch(run_id):
        errors.append("run_id must be a portable non-empty identifier")
    root = data.get("agent_work_root")
    if not isinstance(root, str) or not root or not Path(root).is_absolute():
        errors.append("agent_work_root must be an absolute path")

    operations = data.get("operations")
    if not isinstance(operations, list):
        return errors + ["operations must be a list"]

    expected = data.get("confirmation_sha256")
    if not isinstance(expected, str) or not DIGEST_RE.fullmatch(expected):
        errors.append("confirmation_sha256 is required and must be a lowercase SHA-256 digest")
    elif expected != canonical_digest(data):
        errors.append("confirmation digest mismatch")

    seen_ids: set[str] = set()
    seen_sources: set[str] = set()
    seen_destinations: set[str] = set()
    for index, operation in enumerate(operations):
        if not isinstance(operation, dict):
            errors.append(f"operation {index}: must be an object")
            continue
        kind = operation.get("kind")
        if kind not in {"move_tree", "write_managed_block"}:
            errors.append(f"operation {index}: invalid kind")
        operation_id = operation.get("id")
        if not isinstance(operation_id, str) or not operation_id or operation_id in seen_ids:
            errors.append(f"operation {index}: missing or duplicate id")
        else:
            seen_ids.add(operation_id)

        keys = ("source", "destination") if kind == "move_tree" else ("path",)
        for key in keys:
            value = operation.get(key)
            if not _safe_relative(value):
                errors.append(f"operation {index}: unsafe {key}")

        if kind == "move_tree":
            source = operation.get("source")
            destination = operation.get("destination")
            if isinstance(source, str):
                if source in seen_sources:
                    errors.append(f"operation {index}: duplicate source")
                seen_sources.add(source)
            if isinstance(destination, str):
                if destination in seen_destinations:
                    errors.append(f"operation {index}: duplicate destination")
                seen_destinations.add(destination)
                destination_path = PurePosixPath(destination)
                if destination_path != ARCHIVE_PREFIX and ARCHIVE_PREFIX not in destination_path.parents:
                    errors.append(f"operation {index}: destination must be inside {ARCHIVE_PREFIX.as_posix()}/")
            source_digest = operation.get("source_tree_sha256")
            if not isinstance(source_digest, str) or not DIGEST_RE.fullmatch(source_digest):
                errors.append(f"operation {index}: source_tree_sha256 must be a lowercase SHA-256 digest")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    errors = validate(data)
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    print(f"Validated {len(data.get('operations', [])) if isinstance(data, dict) else 0} operation(s); {len(errors)} error(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
