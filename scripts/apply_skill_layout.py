#!/usr/bin/env python3
"""Apply or roll back the approved digest-bound skill layout migration."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import sys
from pathlib import Path, PurePosixPath
from typing import Any

from prepare_skill_layout import (
    DEFAULT_MANIFEST,
    LayoutMigrationError,
    rewrite_markdown_links,
    validate_manifest,
    write_manifest,
)
from skill_registry import RegistryError, load_registry
from sync_installed_skills import SyncError, file_hashes, tree_digest


DEFAULT_JOURNAL = Path("dist/migration-state/skill-layout-v2-journal.json")
JOURNAL_SCHEMA = 1


def _sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _atomic_bytes(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_bytes(content)
    temporary.replace(path)


def _atomic_json(path: Path, data: dict[str, Any]) -> None:
    _atomic_bytes(path, (json.dumps(data, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))


def _read_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise LayoutMigrationError(f"expected a JSON object: {path}")
    return data


def _require_confirmation(manifest: dict[str, Any], confirmation: str | None) -> None:
    required = f"sha256:{manifest['proposal_sha256']}"
    if confirmation != required:
        raise LayoutMigrationError(f"exact owner confirmation required: --confirm {required}")


def _mappings(repo_root: Path, manifest: dict[str, Any], *, reverse: bool = False) -> list[tuple[Path, Path]]:
    pairs = [
        (
            repo_root / PurePosixPath(move["destination"] if reverse else move["source"]),
            repo_root / PurePosixPath(move["source"] if reverse else move["destination"]),
        )
        for move in manifest["moves"]
    ]
    return pairs


def _rewrite_moved_markdown(repo_root: Path, manifest: dict[str, Any], *, reverse: bool) -> list[dict[str, str]]:
    mappings = _mappings(repo_root, manifest, reverse=reverse)
    rewrites: list[dict[str, str]] = []
    for move in manifest["moves"]:
        before_root = repo_root / PurePosixPath(move["destination"] if reverse else move["source"])
        active_root = repo_root / PurePosixPath(move["destination"])
        after_root = repo_root / PurePosixPath(move["source"] if reverse else move["destination"])
        for active_file in sorted(active_root.rglob("*.md")):
            relative = active_file.relative_to(active_root)
            transformed, file_rewrites = rewrite_markdown_links(
                active_file.read_text(encoding="utf-8"),
                source_file=before_root / relative,
                destination_file=after_root / relative,
                mappings=mappings,
                repo_root=repo_root,
            )
            if file_rewrites:
                active_file.write_text(transformed, encoding="utf-8")
                rewrites.extend(file_rewrites)
    return rewrites


def _verify_tree(path: Path, expected_digest: str, expected_files: int, label: str) -> None:
    hashes = file_hashes(path)
    if tree_digest(hashes) != expected_digest or len(hashes) != expected_files:
        raise LayoutMigrationError(f"{label}: tree digest or file count differs from the approved proposal")


def _journal_snapshot(
    repo_root: Path,
    manifest_path: Path,
    manifest: dict[str, Any],
    registry_bytes: bytes,
    manifest_bytes: bytes,
) -> dict[str, Any]:
    return {
        "schema_version": JOURNAL_SCHEMA,
        "migration": "skill-layout-v2",
        "proposal_sha256": manifest["proposal_sha256"],
        "state": "applying",
        "repo_root": str(repo_root),
        "manifest_path": manifest_path.relative_to(repo_root).as_posix(),
        "registry_before_sha256": _sha256(registry_bytes),
        "manifest_before_sha256": _sha256(manifest_bytes),
        "registry_before_base64": base64.b64encode(registry_bytes).decode("ascii"),
        "manifest_before_base64": base64.b64encode(manifest_bytes).decode("ascii"),
        "registry_after_sha256": None,
        "manifest_after_sha256": None,
        "markdown_rewrites": len(manifest["markdown_link_rewrites"]),
    }


def _validate_journal(journal: dict[str, Any], repo_root: Path, manifest: dict[str, Any]) -> None:
    required = {
        "schema_version",
        "migration",
        "proposal_sha256",
        "state",
        "repo_root",
        "manifest_path",
        "registry_before_sha256",
        "manifest_before_sha256",
        "registry_before_base64",
        "manifest_before_base64",
        "registry_after_sha256",
        "manifest_after_sha256",
        "markdown_rewrites",
    }
    if set(journal) != required or journal.get("schema_version") != JOURNAL_SCHEMA:
        raise LayoutMigrationError("layout journal schema is invalid")
    if journal.get("migration") != "skill-layout-v2" or journal.get("repo_root") != str(repo_root):
        raise LayoutMigrationError("layout journal identity is invalid")
    if journal.get("proposal_sha256") != manifest["proposal_sha256"]:
        raise LayoutMigrationError("layout journal belongs to a different proposal")
    if journal.get("state") not in {"applying", "applied", "rolled-back", "sealed"}:
        raise LayoutMigrationError("layout journal state is invalid")
    try:
        registry_before = base64.b64decode(journal["registry_before_base64"], validate=True)
        manifest_before = base64.b64decode(journal["manifest_before_base64"], validate=True)
    except (ValueError, TypeError) as error:
        raise LayoutMigrationError("layout journal snapshots are invalid") from error
    if _sha256(registry_before) != journal["registry_before_sha256"]:
        raise LayoutMigrationError("layout journal registry snapshot digest mismatch")
    if _sha256(manifest_before) != journal["manifest_before_sha256"]:
        raise LayoutMigrationError("layout journal manifest snapshot digest mismatch")


def _clean_empty_destination_parents(repo_root: Path, manifest: dict[str, Any]) -> None:
    stops = {repo_root, repo_root / "skills"}
    for move in manifest["moves"]:
        current = (repo_root / PurePosixPath(move["destination"])).parent
        while current not in stops and repo_root in current.parents:
            try:
                current.rmdir()
            except OSError:
                break
            current = current.parent


def _preflight_recovery(repo_root: Path, manifest: dict[str, Any]) -> None:
    """Prove every tree is either pristine pre-rewrite or approved post-rewrite."""

    for move in manifest["moves"]:
        source = repo_root / PurePosixPath(move["source"])
        destination = repo_root / PurePosixPath(move["destination"])
        if source.is_dir() and not destination.exists():
            _verify_tree(source, move["source_tree_sha256"], move["source_files"], move["source"])
            continue
        if destination.is_dir() and not source.exists():
            hashes = file_hashes(destination)
            digest = tree_digest(hashes)
            allowed = {
                (move["source_tree_sha256"], move["source_files"]),
                (move["destination_tree_sha256"], move["destination_files"]),
            }
            if (digest, len(hashes)) not in allowed:
                raise LayoutMigrationError(f"{move['destination']}: drift prevents safe rollback")
            continue
        raise LayoutMigrationError(f"{move['name']}: unsafe mixed source/destination state")


def _restore_pre_state(
    repo_root: Path,
    manifest: dict[str, Any],
    journal_path: Path,
    journal: dict[str, Any],
) -> None:
    _preflight_recovery(repo_root, manifest)
    for move in manifest["moves"]:
        source = repo_root / PurePosixPath(move["source"])
        destination = repo_root / PurePosixPath(move["destination"])
        if not destination.is_dir():
            continue
        hashes = file_hashes(destination)
        if tree_digest(hashes) == move["destination_tree_sha256"]:
            _rewrite_moved_markdown_for_one(repo_root, manifest, move, reverse=True)
            _verify_tree(destination, move["source_tree_sha256"], move["source_files"], move["destination"])
        source.parent.mkdir(parents=True, exist_ok=True)
        destination.rename(source)
    registry_path = repo_root / "skills" / "registry.json"
    manifest_path = repo_root / PurePosixPath(journal["manifest_path"])
    _atomic_bytes(registry_path, base64.b64decode(journal["registry_before_base64"], validate=True))
    _atomic_bytes(manifest_path, base64.b64decode(journal["manifest_before_base64"], validate=True))
    _clean_empty_destination_parents(repo_root, manifest)
    restored_registry = load_registry(repo_root)
    restored_manifest = _read_json(manifest_path)
    state, errors = validate_manifest(repo_root, restored_registry, restored_manifest)
    if state != "pre-move" or errors:
        raise LayoutMigrationError("rollback could not re-establish the validated pre-move state: " + "; ".join(errors))
    journal["state"] = "rolled-back"
    _atomic_json(journal_path, journal)


def _rewrite_moved_markdown_for_one(
    repo_root: Path,
    manifest: dict[str, Any],
    move: dict[str, Any],
    *,
    reverse: bool,
) -> None:
    mappings = _mappings(repo_root, manifest, reverse=reverse)
    before_root = repo_root / PurePosixPath(move["destination"] if reverse else move["source"])
    active_root = repo_root / PurePosixPath(move["destination"])
    after_root = repo_root / PurePosixPath(move["source"] if reverse else move["destination"])
    for active_file in sorted(active_root.rglob("*.md")):
        relative = active_file.relative_to(active_root)
        transformed, rewrites = rewrite_markdown_links(
            active_file.read_text(encoding="utf-8"),
            source_file=before_root / relative,
            destination_file=after_root / relative,
            mappings=mappings,
            repo_root=repo_root,
        )
        if rewrites:
            active_file.write_text(transformed, encoding="utf-8")


def apply_layout(
    repo_root: Path,
    manifest_path: Path,
    journal_path: Path,
    confirmation: str,
    *,
    fail_after: int | None = None,
) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    manifest_path = manifest_path.resolve()
    journal_path = journal_path.resolve()
    registry = load_registry(repo_root)
    manifest = _read_json(manifest_path)
    state, errors = validate_manifest(repo_root, registry, manifest)
    if errors or state != "pre-move":
        raise LayoutMigrationError("layout apply requires the validated pre-move state: " + "; ".join(errors))
    _require_confirmation(manifest, confirmation)
    if journal_path.exists():
        existing = _read_json(journal_path)
        _validate_journal(existing, repo_root, manifest)
        if existing["state"] != "rolled-back":
            raise LayoutMigrationError(f"layout journal is already {existing['state']}; recover or roll back first")
    registry_path = registry.path
    registry_bytes = registry_path.read_bytes()
    manifest_bytes = manifest_path.read_bytes()
    journal = _journal_snapshot(repo_root, manifest_path, manifest, registry_bytes, manifest_bytes)
    _atomic_json(journal_path, journal)
    operations = 0

    def checkpoint() -> None:
        nonlocal operations
        operations += 1
        if fail_after is not None and operations >= fail_after:
            raise LayoutMigrationError("injected layout migration failure")

    try:
        for move in manifest["moves"]:
            source = repo_root / PurePosixPath(move["source"])
            destination = repo_root / PurePosixPath(move["destination"])
            destination.parent.mkdir(parents=True, exist_ok=True)
            source.rename(destination)
            checkpoint()
        applied_rewrites = _rewrite_moved_markdown(repo_root, manifest, reverse=False)
        if applied_rewrites != manifest["markdown_link_rewrites"]:
            raise LayoutMigrationError("applied Markdown link rewrites differ from the approved proposal")
        for move in manifest["moves"]:
            _verify_tree(
                repo_root / PurePosixPath(move["destination"]),
                move["destination_tree_sha256"],
                move["destination_files"],
                move["destination"],
            )
        registry_data = json.loads(registry_bytes.decode("utf-8"))
        registry_data["category_model"]["status"] = "approved"
        destinations = {move["name"]: move["destination"] for move in manifest["moves"]}
        for record in registry_data["skills"]:
            record["path"] = destinations[record["name"]]
        _atomic_json(registry_path, registry_data)
        checkpoint()
        manifest["category_model"]["status"] = "approved"
        manifest["status"] = "ready"
        write_manifest(manifest_path, manifest)
        checkpoint()
        moved_registry = load_registry(repo_root)
        state, errors = validate_manifest(repo_root, moved_registry, manifest)
        if state != "post-move" or errors:
            raise LayoutMigrationError("post-move validation failed: " + "; ".join(errors))
        journal["state"] = "applied"
        journal["registry_after_sha256"] = _sha256(registry_path.read_bytes())
        journal["manifest_after_sha256"] = _sha256(manifest_path.read_bytes())
        _atomic_json(journal_path, journal)
        return journal
    except Exception as error:
        try:
            _restore_pre_state(repo_root, manifest, journal_path, journal)
        except Exception as recovery_error:
            raise LayoutMigrationError(f"layout apply failed ({error}); automatic recovery also failed ({recovery_error})") from error
        if isinstance(error, LayoutMigrationError):
            raise
        raise LayoutMigrationError(f"layout apply failed and was rolled back: {error}") from error


def rollback_layout(
    repo_root: Path,
    manifest_path: Path,
    journal_path: Path,
    confirmation: str,
) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    manifest_path = manifest_path.resolve()
    journal_path = journal_path.resolve()
    if not journal_path.is_file():
        raise LayoutMigrationError(f"layout journal is missing: {journal_path}")
    manifest = _read_json(manifest_path)
    journal = _read_json(journal_path)
    _validate_journal(journal, repo_root, manifest)
    _require_confirmation(manifest, confirmation)
    if manifest.get("status") == "completed" or journal["state"] == "sealed":
        raise LayoutMigrationError("layout migration is sealed; restore through version control instead of rollback")
    if journal["state"] != "applied":
        raise LayoutMigrationError(f"layout journal is {journal['state']}; only applied migrations can be rolled back")
    registry_path = repo_root / "skills" / "registry.json"
    if _sha256(registry_path.read_bytes()) != journal["registry_after_sha256"]:
        raise LayoutMigrationError("registry drift prevents rollback")
    if _sha256(manifest_path.read_bytes()) != journal["manifest_after_sha256"]:
        raise LayoutMigrationError("layout manifest drift prevents rollback")
    registry = load_registry(repo_root)
    state, errors = validate_manifest(repo_root, registry, manifest)
    if state != "post-move" or errors:
        raise LayoutMigrationError("layout rollback requires the validated post-move state: " + "; ".join(errors))
    _restore_pre_state(repo_root, manifest, journal_path, journal)
    return journal


def seal_layout(
    repo_root: Path,
    manifest_path: Path,
    journal_path: Path,
    confirmation: str,
) -> dict[str, Any]:
    """Close the rollback window after post-move verification and before normal maintenance."""

    repo_root = repo_root.resolve()
    manifest_path = manifest_path.resolve()
    journal_path = journal_path.resolve()
    manifest = _read_json(manifest_path)
    _require_confirmation(manifest, confirmation)
    if not journal_path.is_file():
        raise LayoutMigrationError(f"layout journal is missing: {journal_path}")
    journal = _read_json(journal_path)
    _validate_journal(journal, repo_root, manifest)
    if manifest.get("status") == "completed" and journal["state"] == "sealed":
        return journal
    if manifest.get("status") != "ready" or journal["state"] != "applied":
        raise LayoutMigrationError("only an applied, ready migration can be sealed")
    candidate = dict(manifest)
    candidate["status"] = "completed"
    registry = load_registry(repo_root)
    state, errors = validate_manifest(repo_root, registry, candidate)
    if state != "post-move" or errors:
        raise LayoutMigrationError("layout seal requires a valid categorized tree: " + "; ".join(errors))
    write_manifest(manifest_path, candidate)
    journal["state"] = "sealed"
    _atomic_json(journal_path, journal)
    return journal


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--apply", action="store_true", help="Apply the approved proposal.")
    action.add_argument("--rollback", action="store_true", help="Roll back an applied proposal.")
    action.add_argument("--seal", action="store_true", help="Seal a verified applied migration before normal maintenance.")
    parser.add_argument("--confirm", help="Exact digest confirmation in sha256:{digest} form.")
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--journal", type=Path)
    args = parser.parse_args(argv)
    repo_root = args.repo_root.resolve()
    manifest_path = (args.manifest or repo_root / DEFAULT_MANIFEST).resolve()
    journal_path = (args.journal or repo_root / DEFAULT_JOURNAL).resolve()
    try:
        manifest = _read_json(manifest_path)
        if not args.apply and not args.rollback and not args.seal:
            registry = load_registry(repo_root)
            state, errors = validate_manifest(repo_root, registry, manifest)
            if errors:
                raise LayoutMigrationError("; ".join(errors))
            required = f"sha256:{manifest['proposal_sha256']}"
            if manifest.get("status") == "completed":
                print(
                    f"SEALED: {len(manifest['moves'])} move(s), {len(manifest['markdown_link_rewrites'])} "
                    f"Markdown rewrite(s), state {state}; proposal {required}."
                )
            else:
                print(
                    f"DRY RUN: {len(manifest['moves'])} move(s), {len(manifest['markdown_link_rewrites'])} "
                    f"Markdown rewrite(s), state {state}. Apply only with --apply --confirm {required}."
                )
            return 0
        if not args.confirm:
            raise LayoutMigrationError("--confirm is required for apply and rollback")
        if args.apply:
            result = apply_layout(repo_root, manifest_path, journal_path, args.confirm)
            print(
                f"Applied {len(manifest['moves'])} layout move(s); proposal sha256 "
                f"{result['proposal_sha256']}; journal {journal_path}."
            )
        elif args.rollback:
            result = rollback_layout(repo_root, manifest_path, journal_path, args.confirm)
            print(
                f"Rolled back {len(manifest['moves'])} layout move(s); proposal sha256 "
                f"{result['proposal_sha256']}; journal {journal_path}."
            )
        else:
            result = seal_layout(repo_root, manifest_path, journal_path, args.confirm)
            print(
                f"Sealed {len(manifest['moves'])} layout move(s); proposal sha256 "
                f"{result['proposal_sha256']}; journal {journal_path}."
            )
    except (OSError, json.JSONDecodeError, RegistryError, LayoutMigrationError, SyncError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
