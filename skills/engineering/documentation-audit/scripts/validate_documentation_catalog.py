#!/usr/bin/env python3
"""Validate Documentation Audit catalog rows supplied as JSON."""

from __future__ import annotations
import argparse, json, sys
from pathlib import Path

FRESHNESS = {"CURRENT", "DRIFTED", "OUTDATED", "UNVERIFIED", "N/A"}
IMPLEMENTATION = {"NOT_IMPLEMENTED", "PARTIALLY_IMPLEMENTED", "IMPLEMENTED", "BLOCKED", "DEFERRED", "REJECTED", "ABANDONED", "SUPERSEDED", "RETIRED", "UNVERIFIED", "N/A"}
AUTHORITY = {"CANONICAL", "SUPPORTING", "HISTORICAL", "DUPLICATE", "CONFLICTING", "UNKNOWN"}
REQUIRED = {"path", "kind", "freshness", "implementation", "authority", "action", "confidence", "evidence"}

def validate(rows: list[dict]) -> list[str]:
    errors, seen = [], set()
    for number, row in enumerate(rows, 1):
        missing = REQUIRED - row.keys()
        if missing: errors.append(f"row {number}: missing {', '.join(sorted(missing))}")
        path = row.get("path")
        if path in seen: errors.append(f"row {number}: duplicate path {path}")
        seen.add(path)
        for key, allowed in (("freshness", FRESHNESS), ("implementation", IMPLEMENTATION), ("authority", AUTHORITY)):
            if row.get(key) not in allowed: errors.append(f"row {number}: invalid {key} {row.get(key)!r}")
        if row.get("freshness") != "UNVERIFIED" and not row.get("evidence"): errors.append(f"row {number}: verified classification lacks evidence")
    return errors

def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("catalog", type=Path); args = parser.parse_args()
    data = json.loads(args.catalog.read_text(encoding="utf-8")); rows = data.get("documents", data) if isinstance(data, dict) else data
    errors = validate(rows)
    for error in errors: print(f"ERROR: {error}", file=sys.stderr)
    print(f"Validated {len(rows)} catalog row(s); {len(errors)} error(s).")
    return 1 if errors else 0
if __name__ == "__main__": raise SystemExit(main())

