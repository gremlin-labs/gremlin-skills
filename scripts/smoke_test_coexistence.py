#!/usr/bin/env python3
"""Prove offline install-order coexistence with synthetic foreign skills."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

from skill_registry import NAME_RE, RegistryError, load_registry
from sync_installed_skills import SyncError, file_hashes, load_manifest, sync_skills, tree_digest


DEFAULT_RECEIPT = Path("dist/validation/coexistence-fixture-receipt.json")
DEFAULT_REFERENCE_NAMES = (
    "foreign-audit-workflow",
    "foreign-build-workflow",
    "foreign-review-workflow",
)
DEFAULT_REFERENCE_REVISION = "synthetic-v1"


class CoexistenceError(RuntimeError):
    """Raised when either installation order changes or collides with foreign content."""


def _reference_bytes(name: str, revision: str) -> bytes:
    return (
        f"---\nname: {name}\ndescription: Synthetic identity fixture for offline coexistence testing only.\n---\n\n"
        f"# {name}\n\nSynthetic fixture revision: `{revision}`.\n"
    ).encode("utf-8")


def _install_reference(target: Path, names: list[str], revision: str) -> None:
    target.mkdir(parents=True, exist_ok=True)
    for name in names:
        destination = target / name
        if destination.exists():
            raise CoexistenceError(f"reference install would overwrite existing identity '{name}'")
        destination.mkdir()
        (destination / "SKILL.md").write_bytes(_reference_bytes(name, revision))


def _digests(target: Path, names: list[str]) -> dict[str, str]:
    return {name: tree_digest(file_hashes(target / name)) for name in names}


def smoke_test(
    repo_root: Path,
    reference_names: list[str] | tuple[str, ...] | None = None,
    *,
    reference_revision: str = DEFAULT_REFERENCE_REVISION,
) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    registry = load_registry(repo_root)
    names = list(DEFAULT_REFERENCE_NAMES if reference_names is None else reference_names)
    if not names or names != sorted(set(names)):
        raise CoexistenceError("synthetic foreign identities must be non-empty, unique, and sorted")
    invalid = [name for name in names if not NAME_RE.fullmatch(name)]
    if invalid:
        raise CoexistenceError(f"invalid synthetic foreign identity: {', '.join(invalid)}")
    gremlin_names = list(registry.names)
    intersections = sorted(set(gremlin_names) & set(names))
    if intersections:
        raise CoexistenceError(f"identity collision prevents clean install: {', '.join(intersections)}")
    order_results: list[dict[str, Any]] = []
    final_gremlin_digests: list[dict[str, str]] = []
    final_reference_digests: list[dict[str, str]] = []
    with tempfile.TemporaryDirectory() as temporary:
        scratch = Path(temporary)
        for order in ("gremlin-then-foreign", "foreign-then-gremlin"):
            target = scratch / order
            if order == "gremlin-then-foreign":
                sync_skills(repo_root, target, None, all_skills=True, apply=True, run_id=f"{order}-gremlin")
                before_gremlin = _digests(target, gremlin_names)
                _install_reference(target, names, reference_revision)
                if _digests(target, gremlin_names) != before_gremlin:
                    raise CoexistenceError("reference installation changed Gremlin-owned content")
            else:
                _install_reference(target, names, reference_revision)
                before_reference = _digests(target, names)
                sync_skills(repo_root, target, None, all_skills=True, apply=True, run_id=f"{order}-gremlin")
                if _digests(target, names) != before_reference:
                    raise CoexistenceError("Gremlin installation changed reference-owned content")
            manifest = load_manifest(target)
            if set(manifest["skills"]) != set(gremlin_names):
                raise CoexistenceError(f"managed manifest ownership is incomplete after {order}")
            visible = {child.name for child in target.iterdir() if child.is_dir() and not child.name.startswith(".")}
            expected = set(gremlin_names) | set(names)
            if visible != expected:
                raise CoexistenceError(f"visible installed identities disagree after {order}")
            gremlin_digests = _digests(target, gremlin_names)
            reference_digests = _digests(target, names)
            final_gremlin_digests.append(gremlin_digests)
            final_reference_digests.append(reference_digests)
            order_results.append({
                "order": order,
                "status": "PASSED",
                "gremlin_skills": len(gremlin_digests),
                "reference_skills": len(reference_digests),
                "managed_owners": len(manifest["skills"]),
            })
    if final_gremlin_digests[0] != final_gremlin_digests[1]:
        raise CoexistenceError("Gremlin content differs by install order")
    if final_reference_digests[0] != final_reference_digests[1]:
        raise CoexistenceError("reference fixture content differs by install order")
    return {
        "schema_version": 1,
        "proof_mode": "offline-synthetic-foreign-library",
        "reference": {
            "kind": "synthetic-foreign-library",
            "revision": reference_revision,
            "skill_records": len(names),
        },
        "gremlin_skill_records": len(gremlin_names),
        "orders": order_results,
        "claims": {
            "identity_intersection_empty": True,
            "foreign_content_unchanged": True,
            "gremlin_content_order_independent": True,
            "real_upstream_installer_exercised": False,
        },
    }


def _atomic_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument(
        "--reference-name",
        action="append",
        help="Synthetic foreign identity to install; repeat for multiple identities.",
    )
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args(argv)
    repo_root = args.repo_root.resolve()
    receipt_path = (args.receipt or repo_root / DEFAULT_RECEIPT).resolve()
    try:
        receipt = smoke_test(repo_root, args.reference_name)
        _atomic_json(receipt_path, receipt)
    except (OSError, RegistryError, SyncError, CoexistenceError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(
        f"Validated both install orders for {receipt['gremlin_skill_records']} Gremlin and "
        f"{receipt['reference']['skill_records']} synthetic foreign identities; receipt {receipt_path}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
