#!/usr/bin/env python3
"""Build and validate a disposable clean Git snapshot of the public source tree."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

from validate_public_release import EXCLUDED_ROOTS, PublicReleaseError, public_files, validate_public_release


DEFAULT_RECEIPT = Path("dist/validation/public-snapshot-receipt.json")


def _git(repo: Path, *arguments: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(repo), *arguments],
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        raise PublicReleaseError(completed.stderr.strip() or f"git {' '.join(arguments)} failed")
    return completed.stdout.strip()


def build_public_snapshot(repo_root: Path, *, require_license: bool = False) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    files, shape_errors = public_files(repo_root)
    if shape_errors:
        raise PublicReleaseError("; ".join(shape_errors))
    with tempfile.TemporaryDirectory(prefix="gremlin-public-snapshot-") as temporary:
        snapshot = Path(temporary) / "repo"
        snapshot.mkdir()
        for source in files:
            relative = source.relative_to(repo_root)
            destination = snapshot / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
        _git(snapshot, "init", "-q", "-b", "main")
        _git(snapshot, "add", "-A")
        count, errors = validate_public_release(snapshot, check_index=True, require_license=require_license)
        if errors:
            raise PublicReleaseError("; ".join(errors))
        staged = [line for line in _git(snapshot, "ls-files").splitlines() if line]
        if len(staged) != count:
            raise PublicReleaseError(
                f"clean snapshot staged {len(staged)} files but the public-tree scanner selected {count}"
            )
        tree_oid = _git(snapshot, "write-tree")
        top_level = sorted({Path(path).parts[0] for path in staged})
        return {
            "schema_version": 1,
            "status": "PASSED",
            "tree_object_format": "sha1",
            "tree_oid": tree_oid,
            "files": len(staged),
            "paths": staged,
            "top_level": top_level,
            "excluded_roots": sorted(EXCLUDED_ROOTS - {".git"}),
            "license_required": require_license,
        }


def write_receipt(path: Path, receipt: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--require-license", action="store_true")
    args = parser.parse_args(argv)
    repo_root = args.repo_root.resolve()
    receipt_path = (args.receipt or repo_root / DEFAULT_RECEIPT).resolve()
    try:
        receipt = build_public_snapshot(repo_root, require_license=args.require_license)
        write_receipt(receipt_path, receipt)
    except (OSError, PublicReleaseError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(
        f"Validated clean public snapshot: {receipt['files']} files, tree {receipt['tree_oid']}; "
        f"receipt {receipt_path}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
