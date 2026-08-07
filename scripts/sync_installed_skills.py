#!/usr/bin/env python3
"""Safely synchronize repository skills into a flat host installation."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from package_skills import EXCLUDED_NAMES, EXCLUDED_SUFFIXES, PackagingError, dependency_closure
from skill_registry import RegistryError, SkillRegistry, load_registry


MANAGED_DIR = ".gremlin-skills"
MANIFEST_NAME = "install-manifest.json"
MANIFEST_SCHEMA = 1


class SyncError(RuntimeError):
    """Raised when installation ownership or recovery cannot be proven."""


def _atomic_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def _included(path: Path, root: Path) -> bool:
    relative = path.relative_to(root)
    return not any(part in EXCLUDED_NAMES for part in relative.parts) and path.suffix not in EXCLUDED_SUFFIXES


def file_hashes(directory: Path) -> dict[str, str]:
    if not directory.is_dir() or directory.is_symlink():
        raise SyncError(f"expected a real skill directory: {directory}")
    hashes: dict[str, str] = {}
    for path in sorted(directory.rglob("*")):
        if not _included(path, directory):
            continue
        if path.is_symlink():
            raise SyncError(f"symbolic links are not installable: {path}")
        if path.is_file():
            hashes[path.relative_to(directory).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    if "SKILL.md" not in hashes:
        raise SyncError(f"skill directory has no SKILL.md: {directory}")
    return hashes


def tree_digest(hashes: dict[str, str]) -> str:
    payload = "".join(f"{path}\0{digest}\n" for path, digest in sorted(hashes.items())).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _empty_manifest(target: Path) -> dict[str, Any]:
    return {
        "schema_version": MANIFEST_SCHEMA,
        "install_root": str(target),
        "skills": {},
        "last_run_id": None,
    }


def load_manifest(target: Path) -> dict[str, Any]:
    target = target.expanduser().resolve()
    path = target / MANAGED_DIR / MANIFEST_NAME
    if not path.exists():
        return _empty_manifest(target)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise SyncError(f"cannot read install manifest {path}: {error}") from error
    if not isinstance(data, dict) or set(data) != {"schema_version", "install_root", "skills", "last_run_id"}:
        raise SyncError(f"invalid install manifest shape: {path}")
    if data["schema_version"] != MANIFEST_SCHEMA or data["install_root"] != str(target):
        raise SyncError(f"install manifest identity mismatch: {path}")
    if not isinstance(data["skills"], dict):
        raise SyncError(f"install manifest skills must be an object: {path}")
    return data


def _validate_target(repo_root: Path, target: Path) -> Path:
    target = target.expanduser().resolve()
    home = Path.home().resolve()
    if target in {Path("/").resolve(), home, repo_root.resolve(), (repo_root / "skills").resolve()}:
        raise SyncError(f"refusing broad or source target: {target}")
    if target.exists() and target.is_symlink():
        raise SyncError(f"install target must not be a symbolic link: {target}")
    return target


def _entry(name: str, hashes: dict[str, str], source_path: str, run_id: str) -> dict[str, Any]:
    return {
        "name": name,
        "source_path": source_path,
        "tree_sha256": tree_digest(hashes),
        "files": hashes,
        "installed_by_run": run_id,
    }


def selected_closure(registry: SkillRegistry, names: list[str] | None, all_skills: bool) -> list[str]:
    if bool(names) == bool(all_skills):
        raise SyncError("choose explicit skill names or --all")
    roots = sorted(set(names or [
        record["name"]
        for record in registry.promoted
        if record["distribution"]["public_install"]
    ]))
    selected: set[str] = set()
    for name in roots:
        record = registry.by_name.get(name)
        if record is None:
            raise SyncError(f"unknown skill '{name}'")
        if record["maturity"] != "promoted" or not record["distribution"]["public_install"]:
            raise SyncError(f"skill '{name}' is not available for stable installation")
        try:
            selected.update(dependency_closure(registry, name))
        except PackagingError as error:
            raise SyncError(str(error)) from error
    return sorted(selected)


def build_plan(
    repo_root: Path,
    target: Path,
    registry: SkillRegistry,
    names: list[str] | None,
    *,
    all_skills: bool,
    retire_deprecated: bool,
    run_id: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    target = _validate_target(repo_root, target)
    manifest = load_manifest(target)
    selected = selected_closure(registry, names, all_skills)
    operations: list[dict[str, Any]] = []
    for name in selected:
        record = registry.by_name[name]
        source = registry.skill_path(record)
        source_hashes = file_hashes(source)
        destination = target / name
        owned = manifest["skills"].get(name)
        if destination.exists() and destination.is_symlink():
            raise SyncError(f"refusing symbolic-link destination: {destination}")
        if destination.exists() and owned is None:
            raise SyncError(f"refusing foreign unowned path: {destination}")
        prior_digest = None
        if owned is not None:
            if not destination.is_dir():
                raise SyncError(f"owned path is missing or not a directory: {destination}")
            current_hashes = file_hashes(destination)
            if current_hashes != owned.get("files") or tree_digest(current_hashes) != owned.get("tree_sha256"):
                raise SyncError(f"refusing locally modified owned skill: {destination}")
            prior_digest = owned["tree_sha256"]
        after_digest = tree_digest(source_hashes)
        action = "install" if owned is None else "noop" if prior_digest == after_digest else "update"
        operations.append({
            "action": action,
            "skill": name,
            "source": record["path"],
            "destination": str(destination),
            "before_sha256": prior_digest,
            "after_sha256": after_digest,
            "files": len(source_hashes),
        })

    retirements: list[dict[str, Any]] = []
    for name in sorted(manifest["skills"]):
        record = registry.by_name.get(name)
        if record is None or record["maturity"] != "deprecated":
            continue
        destination = target / name
        if not retire_deprecated:
            continue
        if not destination.is_dir() or destination.is_symlink():
            raise SyncError(f"cannot retire missing or unsafe owned path: {destination}")
        current_hashes = file_hashes(destination)
        owned = manifest["skills"][name]
        if current_hashes != owned.get("files") or tree_digest(current_hashes) != owned.get("tree_sha256"):
            raise SyncError(f"refusing to retire locally modified skill: {destination}")
        retirements.append({
            "action": "retire",
            "skill": name,
            "destination": str(destination),
            "before_sha256": owned["tree_sha256"],
            "after_sha256": None,
            "files": len(current_hashes),
        })

    plan = {
        "schema_version": 1,
        "run_id": run_id,
        "mode": "apply" if False else "dry-run",
        "repo_root": str(repo_root),
        "target": str(target),
        "selected": selected,
        "retire_deprecated": retire_deprecated,
        "operations": operations + retirements,
    }
    return plan, manifest


def _copy_source(source: Path, stage: Path) -> None:
    if stage.exists():
        raise SyncError(f"staging collision: {stage}")
    shutil.copytree(
        source,
        stage,
        ignore=shutil.ignore_patterns(*EXCLUDED_NAMES, "*.pyc", "*.pyo"),
    )
    file_hashes(stage)


def apply_plan(
    repo_root: Path,
    target: Path,
    registry: SkillRegistry,
    plan: dict[str, Any],
    manifest: dict[str, Any],
    *,
    fail_after: int | None = None,
) -> dict[str, Any]:
    target.mkdir(parents=True, exist_ok=True)
    managed = target / MANAGED_DIR
    run_id = plan["run_id"]
    backup_root = managed / "backups" / run_id
    staging_root = managed / "staging" / run_id
    journal_path = managed / "runs" / f"{run_id}.json"
    manifest_before = json.loads(json.dumps(manifest))
    journal = {
        "schema_version": 1,
        "run_id": run_id,
        "target": str(target),
        "status": "applying",
        "manifest_before": manifest_before,
        "operations": [dict(operation, state="pending") for operation in plan["operations"]],
    }
    _atomic_json(journal_path, journal)
    applied = 0
    try:
        for index, operation in enumerate(journal["operations"]):
            if operation["action"] == "noop":
                operation["state"] = "skipped"
                _atomic_json(journal_path, journal)
                continue
            name = operation["skill"]
            destination = target / name
            backup = backup_root / name
            if operation["action"] in {"install", "update"}:
                source = registry.skill_path(name)
                stage = staging_root / name
                stage.parent.mkdir(parents=True, exist_ok=True)
                _copy_source(source, stage)
                if tree_digest(file_hashes(stage)) != operation["after_sha256"]:
                    raise SyncError(f"staged source changed during apply: {name}")
                if destination.exists():
                    backup.parent.mkdir(parents=True, exist_ok=True)
                    destination.replace(backup)
                try:
                    stage.replace(destination)
                except BaseException:
                    if backup.exists() and not destination.exists():
                        backup.replace(destination)
                    raise
                hashes = file_hashes(destination)
                manifest["skills"][name] = _entry(
                    name, hashes, registry.by_name[name]["path"], run_id
                )
            elif operation["action"] == "retire":
                if name not in manifest["skills"]:
                    raise SyncError(f"retirement lost manifest ownership: {name}")
                backup.parent.mkdir(parents=True, exist_ok=True)
                destination.replace(backup)
                del manifest["skills"][name]
            else:
                raise SyncError(f"unknown sync action: {operation['action']}")
            operation["state"] = "applied"
            applied += 1
            manifest["last_run_id"] = run_id
            _atomic_json(managed / MANIFEST_NAME, manifest)
            _atomic_json(journal_path, journal)
            if fail_after is not None and applied >= fail_after:
                raise SyncError(f"simulated interruption after {applied} applied operation(s)")
        journal["status"] = "complete"
        _atomic_json(journal_path, journal)
        if staging_root.exists():
            shutil.rmtree(staging_root)
        return journal
    except BaseException as error:
        journal["status"] = "recovery-required"
        journal["error"] = str(error)
        _atomic_json(journal_path, journal)
        raise


def rollback_run(target: Path, run_id: str) -> dict[str, Any]:
    target = target.expanduser().resolve()
    managed = target / MANAGED_DIR
    journal_path = managed / "runs" / f"{run_id}.json"
    try:
        journal = json.loads(journal_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise SyncError(f"cannot read rollback journal: {error}") from error
    if journal.get("target") != str(target) or journal.get("status") not in {"complete", "recovery-required"}:
        raise SyncError("rollback journal identity or state is not eligible")
    rollback_root = managed / "rollback-removed" / run_id
    for operation in reversed(journal["operations"]):
        if operation.get("state") != "applied":
            continue
        name = operation["skill"]
        destination = target / name
        backup = managed / "backups" / run_id / name
        if operation["action"] in {"install", "update"}:
            if not destination.is_dir() or destination.is_symlink():
                raise SyncError(f"cannot rollback missing or unsafe destination: {destination}")
            current_digest = tree_digest(file_hashes(destination))
            if current_digest != operation["after_sha256"]:
                raise SyncError(f"refusing rollback of modified installed skill: {destination}")
            removed = rollback_root / name
            removed.parent.mkdir(parents=True, exist_ok=True)
            destination.replace(removed)
            if operation["action"] == "update":
                if not backup.is_dir():
                    removed.replace(destination)
                    raise SyncError(f"rollback backup is missing: {backup}")
                backup.replace(destination)
        elif operation["action"] == "retire":
            if destination.exists() or not backup.is_dir():
                raise SyncError(f"cannot restore retired skill safely: {name}")
            backup.replace(destination)
        operation["state"] = "rolled-back"
        _atomic_json(journal_path, journal)
    manifest_before = journal.get("manifest_before")
    if not isinstance(manifest_before, dict):
        raise SyncError("rollback journal has no valid prior manifest")
    _atomic_json(managed / MANIFEST_NAME, manifest_before)
    journal["status"] = "rolled-back"
    _atomic_json(journal_path, journal)
    return journal


def sync_skills(
    repo_root: Path,
    target: Path,
    names: list[str] | None = None,
    *,
    all_skills: bool = False,
    apply: bool = False,
    retire_deprecated: bool = False,
    run_id: str | None = None,
    fail_after: int | None = None,
) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    target = _validate_target(repo_root, target)
    try:
        registry = load_registry(repo_root)
    except RegistryError as error:
        raise SyncError(str(error)) from error
    run_id = run_id or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:12]
    plan, manifest = build_plan(
        repo_root,
        target,
        registry,
        names,
        all_skills=all_skills,
        retire_deprecated=retire_deprecated,
        run_id=run_id,
    )
    plan["mode"] = "apply" if apply else "dry-run"
    if not apply:
        return plan
    return apply_plan(repo_root, target, registry, plan, manifest, fail_after=fail_after)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skills", nargs="*", help="Explicit root skill names; required unless --all or --rollback.")
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--all", action="store_true", help="Select every promoted public-install skill.")
    parser.add_argument("--dry-run", action="store_true", help="Explicitly select the default no-write mode.")
    parser.add_argument("--apply", action="store_true", help="Apply the exact preflighted operations.")
    parser.add_argument("--retire-deprecated", action="store_true", help="Retire only manifest-owned deprecated skills.")
    parser.add_argument("--rollback", metavar="RUN_ID", help="Rollback one completed or interrupted run.")
    args = parser.parse_args(argv)
    if args.apply and args.dry_run:
        parser.error("choose --apply or --dry-run")
    try:
        if args.rollback:
            if args.skills or args.all or args.apply or args.retire_deprecated:
                parser.error("--rollback cannot be combined with selection or apply options")
            result = rollback_run(args.target, args.rollback)
        else:
            all_skills = args.all or (not args.skills and not args.apply)
            result = sync_skills(
                args.repo_root,
                args.target,
                args.skills,
                all_skills=all_skills,
                apply=args.apply,
                retire_deprecated=args.retire_deprecated,
            )
    except (OSError, SyncError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
