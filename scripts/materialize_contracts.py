#!/usr/bin/env python3
"""Materialize digest-stamped root contract snapshots into dependent skills."""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from skill_registry import RegistryError, SkillRegistry, load_registry


GENERATED_PREFIX = "<!-- GENERATED CONTRACT SNAPSHOT\n"
METADATA_RE = re.compile(
    r"\A<!-- contract-metadata\nid: ([a-z0-9-]+)\nversion: ([1-9][0-9]*)\nsemantic-owner: ([a-z0-9-]+)\n-->\n",
)


@dataclass(frozen=True)
class ContractDefinition:
    registry_id: str
    source: str
    snapshot: str
    required_contracts: tuple[str, ...] = ()


CONTRACTS = {
    definition.registry_id: definition
    for definition in (
        ContractDefinition("work-artifacts", "contracts/work-artifacts.md", "work-artifacts.md"),
        ContractDefinition("quality", "contracts/execution-quality.md", "execution-quality.md"),
        ContractDefinition(
            "product-research",
            "contracts/product-research.md",
            "product-research.md",
            ("quality",),
        ),
        ContractDefinition(
            "goalpro-handoff",
            "contracts/goalpro-handoff.md",
            "goalpro-handoff.md",
            ("quality",),
        ),
    )
}


class ContractMaterializationError(RuntimeError):
    """Raised when a source or generated contract cannot be trusted."""


def source_metadata(source: Path, definition: ContractDefinition) -> tuple[int, str]:
    text = source.read_text(encoding="utf-8")
    match = METADATA_RE.match(text)
    if not match:
        raise ContractMaterializationError(f"{source}: missing exact contract metadata header")
    contract_id, version, owner = match.groups()
    expected_id = "execution-quality" if definition.registry_id == "quality" else definition.registry_id
    if contract_id != expected_id:
        raise ContractMaterializationError(
            f"{source}: metadata id '{contract_id}' does not match expected '{expected_id}'"
        )
    return int(version), owner


def snapshot_bytes(repo_root: Path, definition: ContractDefinition) -> bytes:
    source = repo_root / definition.source
    source_bytes = source.read_bytes()
    version, owner = source_metadata(source, definition)
    digest = hashlib.sha256(source_bytes).hexdigest()
    header = (
        GENERATED_PREFIX
        + f"contract: {definition.registry_id}\n"
        + f"source: {definition.source}\n"
        + f"source-version: {version}\n"
        + f"semantic-owner: {owner}\n"
        + f"source-sha256: {digest}\n"
        + "DO NOT EDIT: run python3 scripts/materialize_contracts.py --write\n"
        + "-->\n\n"
    ).encode("utf-8")
    return header + source_bytes


def expected_snapshots(repo_root: Path, registry: SkillRegistry) -> dict[Path, bytes]:
    repo_root = repo_root.resolve()
    expected: dict[Path, bytes] = {}
    payloads = {name: snapshot_bytes(repo_root, definition) for name, definition in CONTRACTS.items()}
    for record in registry.records:
        declared = set(record["contracts"])
        unknown = sorted(declared - CONTRACTS.keys())
        if unknown:
            raise ContractMaterializationError(
                f"registry skill '{record['name']}': unknown contract(s): {', '.join(unknown)}"
            )
        for contract_id in sorted(declared):
            definition = CONTRACTS[contract_id]
            missing = sorted(set(definition.required_contracts) - declared)
            if missing:
                raise ContractMaterializationError(
                    f"registry skill '{record['name']}': contract '{contract_id}' requires {', '.join(missing)}"
                )
            target = registry.skill_path(record) / "contracts" / definition.snapshot
            expected[target] = payloads[contract_id]
    return expected


def generated_snapshot_paths(registry: SkillRegistry) -> set[Path]:
    paths: set[Path] = set()
    for record in registry.records:
        directory = registry.skill_path(record) / "contracts"
        if not directory.is_dir():
            continue
        for path in directory.glob("*.md"):
            if path.read_bytes().startswith(GENERATED_PREFIX.encode("utf-8")):
                paths.add(path)
    return paths


def check_materialized(repo_root: Path, registry: SkillRegistry) -> list[str]:
    repo_root = repo_root.resolve()
    errors: list[str] = []
    try:
        expected = expected_snapshots(repo_root, registry)
    except (OSError, UnicodeDecodeError, ContractMaterializationError) as error:
        return [str(error)]
    actual_generated = generated_snapshot_paths(registry)
    for path, payload in expected.items():
        if not path.is_file():
            errors.append(f"missing generated contract snapshot: {path.relative_to(repo_root)}")
        elif path.read_bytes() != payload:
            errors.append(f"stale generated contract snapshot: {path.relative_to(repo_root)}")
    for path in sorted(actual_generated - expected.keys()):
        errors.append(f"undeclared generated contract snapshot: {path.relative_to(repo_root)}")
    return errors


def write_materialized(repo_root: Path, registry: SkillRegistry) -> tuple[int, int]:
    repo_root = repo_root.resolve()
    expected = expected_snapshots(repo_root, registry)
    actual_generated = generated_snapshot_paths(registry)
    written = 0
    removed = 0
    for path, payload in expected.items():
        if path.is_file() and path.read_bytes() == payload:
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_name(f".{path.name}.tmp")
        temporary.write_bytes(payload)
        temporary.replace(path)
        written += 1
    for path in sorted(actual_generated - expected.keys()):
        path.unlink()
        removed += 1
        if not any(path.parent.iterdir()):
            path.parent.rmdir()
    return written, removed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--write", action="store_true", help="Atomically refresh generated snapshots.")
    parser.add_argument("--check", action="store_true", help="Explicit check mode (the default).")
    args = parser.parse_args(argv)
    if args.write and args.check:
        parser.error("choose either --write or --check")
    repo_root = args.repo_root.resolve()
    try:
        registry = load_registry(repo_root)
        if args.write:
            written, removed = write_materialized(repo_root, registry)
            print(f"Materialized {written} contract snapshot(s); removed {removed} stale generated snapshot(s).")
            return 0
        errors = check_materialized(repo_root, registry)
    except (RegistryError, ContractMaterializationError, OSError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Contract materialization check failed: {len(errors)} error(s).", file=sys.stderr)
        return 1
    count = len(expected_snapshots(repo_root, registry))
    print(f"Validated {count} generated contract snapshot(s) for {len(registry.records)} skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
