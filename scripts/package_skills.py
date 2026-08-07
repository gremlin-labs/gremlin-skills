#!/usr/bin/env python3
"""Build deterministic, independently installable skill ZIP archives."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path

from materialize_contracts import check_materialized
from skill_registry import RegistryError, load_registry
from validate_registry import validate_registry
from validate_skills import validate_repo


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SKILLS_ROOT = REPO_ROOT / "skills"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "dist" / "claude-code-skills"
EXCLUDED_NAMES = {".DS_Store", "__pycache__", ".git"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}
ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")


class PackagingError(RuntimeError):
    """Raised when a skill cannot be packaged safely."""


def package_version(repo_root: Path) -> str:
    path = repo_root / "package.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise PackagingError(f"{path}: {error}") from error
    version = data.get("version") if isinstance(data, dict) else None
    if not isinstance(version, str) or not SEMVER_RE.fullmatch(version):
        raise PackagingError(f"{path}: missing semantic version")
    return version


def discover_skills(skills_root: Path) -> dict[str, Path]:
    try:
        registry = load_registry(skills_root.parent)
    except RegistryError as error:
        raise PackagingError(f"registry discovery failed:\n{error}") from error
    registered_paths = {registry.skill_path(record) for record in registry.records}
    physical_paths = {path.parent.resolve() for path in skills_root.rglob("SKILL.md") if path.is_file()}
    unregistered = sorted(path.relative_to(skills_root) for path in physical_paths - registered_paths)
    missing = sorted(path.relative_to(skills_root) for path in registered_paths - physical_paths)
    if unregistered:
        raise PackagingError(f"unregistered skill source(s): {', '.join(map(str, unregistered))}")
    if missing:
        raise PackagingError(f"registered skill source(s) missing: {', '.join(map(str, missing))}")
    discovered: dict[str, Path] = {}
    for record in registry.records:
        if not record["distribution"]["standalone_archive"]:
            continue
        path = registry.skill_path(record)
        if path != skills_root and skills_root not in path.parents:
            raise PackagingError(f"registry path for {record['name']} is outside {skills_root}")
        discovered[record["name"]] = path
    return discovered


def included_files(skill_dir: Path) -> list[Path]:
    files: list[Path] = []
    for path in sorted(skill_dir.rglob("*")):
        relative = path.relative_to(skill_dir)
        if any(part in EXCLUDED_NAMES for part in relative.parts):
            continue
        if path.is_symlink():
            raise PackagingError(f"{skill_dir.name}: symbolic links are not portable: {relative}")
        if path.is_file() and path.suffix not in EXCLUDED_SUFFIXES:
            files.append(path)
    if not files or not (skill_dir / "SKILL.md").is_file():
        raise PackagingError(f"{skill_dir.name}: missing SKILL.md")
    return files


def zip_info(archive_path: str, executable: bool) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(archive_path, ZIP_TIMESTAMP)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3
    info.external_attr = (0o100755 if executable else 0o100644) << 16
    return info


def dependency_closure(registry, root_name: str) -> list[str]:
    """Return deterministic required-skill closure or reject a cycle."""

    by_name = registry.by_name
    resolved: set[str] = set()
    visiting: list[str] = []

    def visit(name: str) -> None:
        if name in resolved:
            return
        if name in visiting:
            start = visiting.index(name)
            cycle = " -> ".join(visiting[start:] + [name])
            raise PackagingError(f"unsupported required dependency cycle: {cycle}")
        record = by_name.get(name)
        if record is None:
            raise PackagingError(f"unknown required dependency '{name}'")
        if not record["distribution"]["standalone_archive"]:
            raise PackagingError(f"required dependency '{name}' is excluded from standalone archives")
        visiting.append(name)
        for dependency in record["dependencies"]["required_skills"]:
            visit(dependency)
        visiting.pop()
        resolved.add(name)

    visit(root_name)
    return sorted(resolved)


def package_skill(
    root_name: str,
    closure: list[str],
    skill_dirs: dict[str, Path],
    output_dir: Path,
) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    archive = output_dir / f"{root_name}.zip"
    temporary = output_dir / f".{root_name}.zip.tmp"
    closure_files = {name: included_files(skill_dirs[name]) for name in closure}
    try:
        with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
            for name in closure:
                skill_dir = skill_dirs[name]
                for path in closure_files[name]:
                    relative = path.relative_to(skill_dir)
                    archive_path = (Path(name) / relative).as_posix()
                    executable = bool(path.stat().st_mode & 0o111)
                    bundle.writestr(zip_info(archive_path, executable), path.read_bytes(), compresslevel=9)
        temporary.replace(archive)
    finally:
        temporary.unlink(missing_ok=True)
    payload = archive.read_bytes()
    return {
        "skill": root_name,
        "closure": closure,
        "archive": archive.name,
        "sha256": hashlib.sha256(payload).hexdigest(),
        "bytes": len(payload),
        "files": sum(len(files) for files in closure_files.values()),
    }


def package_skills(
    skills_root: Path,
    output_dir: Path,
    requested: list[str] | None = None,
    *,
    clean: bool = False,
    validate: bool = True,
) -> list[dict[str, object]]:
    skills_root = skills_root.resolve()
    output_dir = output_dir.resolve()
    if output_dir == skills_root or skills_root in output_dir.parents:
        raise PackagingError("output directory must be outside skills/ to prevent recursive archives")
    available = discover_skills(skills_root)
    try:
        registry = load_registry(skills_root.parent)
    except RegistryError as error:
        raise PackagingError(f"registry discovery failed:\n{error}") from error
    names = sorted(set(requested or available))
    unknown = sorted(set(names) - available.keys())
    if unknown:
        raise PackagingError(f"unknown skill(s): {', '.join(unknown)}")
    if not names:
        raise PackagingError("no skills found")

    if validate:
        repo_root = skills_root.parent
        validated, errors = validate_repo(repo_root)
        if errors:
            raise PackagingError("repository validation failed:\n" + "\n".join(errors))
        if sorted(validated) != sorted(available):
            raise PackagingError("validated skill inventory differs from packaging inventory")
        registry_errors = validate_registry(repo_root, registry)
        if registry_errors:
            raise PackagingError("registry validation failed:\n" + "\n".join(registry_errors))
        contract_errors = check_materialized(repo_root, registry)
        if contract_errors:
            raise PackagingError("contract materialization failed:\n" + "\n".join(contract_errors))

    output_dir.mkdir(parents=True, exist_ok=True)
    if clean:
        safe_archives = {f"{name}.zip" for name in available}
        manifest_path = output_dir / "manifest.json"
        if manifest_path.is_file():
            try:
                previous = json.loads(manifest_path.read_text(encoding="utf-8"))
                safe_archives.update(
                    Path(record["archive"]).name
                    for record in previous.get("skills", [])
                    if isinstance(record, dict) and str(record.get("archive", "")).endswith(".zip")
                )
            except (json.JSONDecodeError, OSError, TypeError):
                pass
        for name in safe_archives:
            (output_dir / name).unlink(missing_ok=True)
        manifest_path.unlink(missing_ok=True)

    records = [
        package_skill(name, dependency_closure(registry, name), available, output_dir)
        for name in names
    ]
    manifest = {
        "schemaVersion": 3,
        "packageVersion": package_version(skills_root.parent),
        "archiveLayout": "Each ZIP contains the root skill and its required skill closure as flat top-level {skill-name}/ folders.",
        "requested": names,
        "skills": records,
    }
    (output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return records


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skills", nargs="*", help="Skill names to package; omit to package every skill.")
    parser.add_argument("--skills-root", type=Path, default=DEFAULT_SKILLS_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--clean", action="store_true", help="Remove stale ZIPs from the output directory first.")
    parser.add_argument("--skip-validation", action="store_true", help="Skip repository validation (not recommended).")
    args = parser.parse_args(argv)
    try:
        records = package_skills(
            args.skills_root,
            args.output_dir,
            args.skills,
            clean=args.clean,
            validate=not args.skip_validation,
        )
    except (OSError, PackagingError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    for record in records:
        print(f"{record['skill']}: {record['archive']} ({record['files']} files, sha256 {record['sha256']})")
    print(f"Wrote {len(records)} archive(s) and manifest to {args.output_dir.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
