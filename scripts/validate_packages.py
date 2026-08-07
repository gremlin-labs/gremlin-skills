#!/usr/bin/env python3
"""Validate deterministic standalone archives after extraction outside the repository."""

from __future__ import annotations

import argparse
import hashlib
import json
import stat
import sys
import tempfile
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any

from materialize_contracts import CONTRACTS, snapshot_bytes
from package_skills import PackagingError, dependency_closure, package_version
from skill_registry import RegistryError, load_registry
from validate_skills import validate_skill


ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
RECORD_FIELDS = {"skill", "closure", "archive", "sha256", "bytes", "files"}


def _load_manifest(path: Path) -> tuple[dict[str, Any] | None, list[str]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return None, [f"{path}: {error}"]
    if not isinstance(data, dict):
        return None, [f"{path}: expected an object"]
    expected = {"schemaVersion", "packageVersion", "archiveLayout", "requested", "skills"}
    missing = sorted(expected - data.keys())
    unknown = sorted(data.keys() - expected)
    errors = []
    if missing:
        errors.append(f"{path}: missing field(s): {', '.join(missing)}")
    if unknown:
        errors.append(f"{path}: unknown field(s): {', '.join(unknown)}")
    if data.get("schemaVersion") != 3:
        errors.append(f"{path}: expected schemaVersion 3")
    if not isinstance(data.get("requested"), list) or data.get("requested") != sorted(set(data.get("requested", []))):
        errors.append(f"{path}: requested must be a unique sorted array")
    if not isinstance(data.get("skills"), list):
        errors.append(f"{path}: skills must be an array")
    return data, errors


def _safe_members(bundle: zipfile.ZipFile, archive: Path, closure: set[str]) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    for info in bundle.infolist():
        name = info.filename
        pure = PurePosixPath(name)
        if name in seen:
            errors.append(f"{archive}: duplicate member '{name}'")
        seen.add(name)
        if pure.is_absolute() or ".." in pure.parts or "." in pure.parts or len(pure.parts) < 2:
            errors.append(f"{archive}: unsafe or unscoped member '{name}'")
            continue
        if pure.parts[0] not in closure:
            errors.append(f"{archive}: member '{name}' is outside declared closure")
        mode = info.external_attr >> 16
        if stat.S_ISLNK(mode):
            errors.append(f"{archive}: symbolic-link member '{name}' is forbidden")
        if info.date_time != ZIP_TIMESTAMP:
            errors.append(f"{archive}: member '{name}' has nondeterministic timestamp {info.date_time}")
    if set(PurePosixPath(name).parts[0] for name in seen if PurePosixPath(name).parts) != closure:
        errors.append(f"{archive}: top-level folders do not match declared closure")
    return errors


def validate_packages(repo_root: Path, package_dir: Path) -> tuple[int, list[str]]:
    repo_root = repo_root.resolve()
    package_dir = package_dir.resolve()
    try:
        registry = load_registry(repo_root)
        version = package_version(repo_root)
    except RegistryError as error:
        return 0, str(error).splitlines()
    except PackagingError as error:
        return 0, [str(error)]
    data, errors = _load_manifest(package_dir / "manifest.json")
    if data is None:
        return 0, errors
    if data.get("packageVersion") != version:
        errors.append(f"manifest: packageVersion {data.get('packageVersion')!r} does not match {version!r}")
    records = data.get("skills", []) if isinstance(data.get("skills"), list) else []
    requested = data.get("requested", []) if isinstance(data.get("requested"), list) else []
    record_names = [record.get("skill") for record in records if isinstance(record, dict)]
    if record_names != requested:
        errors.append("manifest: skill record order must exactly match requested")
    if len(record_names) != len(set(record_names)):
        errors.append("manifest: duplicate root skill record")

    for index, record in enumerate(records):
        location = f"manifest.skills[{index}]"
        if not isinstance(record, dict):
            errors.append(f"{location}: expected an object")
            continue
        if set(record) != RECORD_FIELDS:
            errors.append(f"{location}: expected fields {', '.join(sorted(RECORD_FIELDS))}")
            continue
        name = record["skill"]
        if name not in registry.by_name:
            errors.append(f"{location}: unknown root skill '{name}'")
            continue
        try:
            expected_closure = dependency_closure(registry, name)
        except PackagingError as error:
            errors.append(f"{location}: {error}")
            continue
        closure = record["closure"]
        if closure != expected_closure:
            errors.append(f"{location}: closure {closure!r} does not match {expected_closure!r}")
            closure = expected_closure
        archive_name = record["archive"]
        if not isinstance(archive_name, str) or Path(archive_name).name != archive_name or archive_name != f"{name}.zip":
            errors.append(f"{location}: invalid archive name '{archive_name}'")
            continue
        archive = package_dir / archive_name
        if not archive.is_file():
            errors.append(f"{location}: archive is missing: {archive_name}")
            continue
        payload = archive.read_bytes()
        if record["sha256"] != hashlib.sha256(payload).hexdigest():
            errors.append(f"{location}: archive checksum mismatch")
        if record["bytes"] != len(payload):
            errors.append(f"{location}: archive byte count mismatch")

        try:
            with zipfile.ZipFile(archive) as bundle:
                infos = bundle.infolist()
                if record["files"] != len(infos):
                    errors.append(f"{location}: archive file count mismatch")
                errors.extend(_safe_members(bundle, archive, set(closure)))
                if any(error.startswith(str(archive)) and "unsafe" in error for error in errors):
                    continue
                with tempfile.TemporaryDirectory(prefix=f"gremlin-package-{name}-") as temporary:
                    extracted = Path(temporary)
                    bundle.extractall(extracted)
                    fake_readme = "# Package\n\n" + "\n".join(
                        f"└── {skill}/\n\n### {skill} package" for skill in closure
                    )
                    for skill_name in closure:
                        skill_record = registry.by_name[skill_name]
                        skill_dir = extracted / skill_name
                        if not (skill_dir / "SKILL.md").is_file():
                            errors.append(f"{location}: extracted closure skill '{skill_name}' is missing SKILL.md")
                            continue
                        errors.extend(validate_skill(skill_dir, fake_readme, skill_record))
                        for contract_id in skill_record["contracts"]:
                            definition = CONTRACTS[contract_id]
                            snapshot = skill_dir / "contracts" / definition.snapshot
                            expected = snapshot_bytes(repo_root, definition)
                            if not snapshot.is_file() or snapshot.read_bytes() != expected:
                                errors.append(
                                    f"{location}: extracted '{skill_name}' has missing or stale contract '{contract_id}'"
                                )
        except (OSError, zipfile.BadZipFile) as error:
            errors.append(f"{location}: cannot inspect archive: {error}")
    return len(records), errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--package-dir", type=Path)
    args = parser.parse_args(argv)
    repo_root = args.repo_root.resolve()
    package_dir = (args.package_dir or repo_root / "dist" / "claude-code-skills").resolve()
    count, errors = validate_packages(repo_root, package_dir)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Package validation failed: {len(errors)} error(s).", file=sys.stderr)
        return 1
    print(f"Validated {count} extracted dependency-complete archive(s) in {package_dir}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
