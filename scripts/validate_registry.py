#!/usr/bin/env python3
"""Validate registry coverage against source, eval contracts, tests, and links."""

from __future__ import annotations

import argparse
import json
import re
import shlex
import sys
from pathlib import Path

from skill_registry import RegistryError, SkillRegistry, load_registry


FRONTMATTER_NAME_RE = re.compile(r"^name:\s*([^\s]+)\s*$", re.MULTILINE)
SIBLING_SKILL_LINK_RE = re.compile(r"\.\./([a-z0-9]+(?:-[a-z0-9]+)*)/(?:SKILL|REFERENCE)\.md")
LOCAL_CONTRACT_LINK_RE = re.compile(
    r"\(contracts/(work-artifacts|product-research|execution-quality|goalpro-handoff|seo-page-quality)\.md\)"
)
CONTRACT_FILE_TO_ID = {
    "work-artifacts": "work-artifacts",
    "product-research": "product-research",
    "execution-quality": "quality",
    "goalpro-handoff": "goalpro-handoff",
    "seo-page-quality": "seo-page-quality",
}


def _load_artifact_roots(repo_root: Path) -> tuple[dict[str, str], list[str]]:
    path = repo_root / "evals" / "artifact-contracts.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return {}, [f"{path}: {error}"]
    contracts = data.get("contracts") if isinstance(data, dict) else None
    if not isinstance(contracts, list):
        return {}, [f"{path}: expected contracts array"]
    roots: dict[str, str] = {}
    errors: list[str] = []
    for index, contract in enumerate(contracts):
        if not isinstance(contract, dict):
            errors.append(f"{path}:contracts[{index}]: expected object")
            continue
        name = contract.get("skill")
        root = contract.get("output_root")
        if isinstance(name, str) and isinstance(root, str):
            if name in roots:
                errors.append(f"{path}: duplicate artifact contract for '{name}'")
            roots[name] = root
    return roots, errors


def _declared_command_paths(command: str) -> set[str]:
    try:
        tokens = shlex.split(command)
    except ValueError:
        return set()
    return {token for token in tokens if "/" in token and not token.startswith("-")}


def _skill_test_paths(repo_root: Path, skill_path: Path) -> set[str]:
    scripts = skill_path / "scripts"
    if not scripts.is_dir():
        return set()
    result: set[str] = set()
    for path in scripts.rglob("*"):
        if "__pycache__" in path.parts:
            continue
        if path.is_file() and (
            path.name in {"test_tools.py", "test-tools.mjs"} or path.name.startswith("test_") and path.suffix == ".py"
        ):
            result.add(path.relative_to(repo_root).as_posix())
    return result


def validate_registry(repo_root: Path, registry: SkillRegistry | None = None) -> list[str]:
    repo_root = repo_root.resolve()
    errors: list[str] = []
    if registry is None:
        try:
            registry = load_registry(repo_root)
        except RegistryError as error:
            return str(error).splitlines()

    expected_paths = {record["path"] for record in registry.records}
    discovered_paths = {
        path.parent.relative_to(repo_root).as_posix()
        for path in (repo_root / "skills").rglob("SKILL.md")
        if path.is_file()
    }
    for path in sorted(discovered_paths - expected_paths):
        errors.append(f"unregistered skill source: {path}")
    for path in sorted(expected_paths - discovered_paths):
        errors.append(f"registered skill source is missing: {path}")

    artifact_roots, artifact_errors = _load_artifact_roots(repo_root)
    errors.extend(artifact_errors)
    known_names = set(registry.names)
    for record in registry.records:
        name = record["name"]
        location = f"registry skill '{name}'"
        skill_path = registry.skill_path(record)
        if skill_path.name != name:
            errors.append(f"{location}: source directory basename must remain '{name}'")
        skill_file = skill_path / "SKILL.md"
        if not skill_file.is_file():
            continue
        text = skill_file.read_text(encoding="utf-8")
        match = FRONTMATTER_NAME_RE.search(text)
        if not match or match.group(1) != name:
            errors.append(f"{location}: SKILL.md frontmatter name does not match")

        actual_root = artifact_roots.get(name)
        if actual_root != record["output_root"]:
            errors.append(
                f"{location}: registry output_root {record['output_root']!r} does not match artifact contract {actual_root!r}"
            )

        linked_skills = {
            dependency for dependency in SIBLING_SKILL_LINK_RE.findall(text) if dependency in known_names
        }
        declared_dependencies = set(record["dependencies"]["required_skills"]) | set(
            record["dependencies"]["optional_skills"]
        )
        for dependency in sorted(linked_skills - declared_dependencies):
            errors.append(f"{location}: linked skill '{dependency}' is not declared as a dependency")

        linked_contracts: set[str] = set()
        for markdown in skill_path.rglob("*.md"):
            if markdown.parent == skill_path / "contracts":
                continue
            linked_contracts.update(
                CONTRACT_FILE_TO_ID[contract_name]
                for contract_name in LOCAL_CONTRACT_LINK_RE.findall(markdown.read_text(encoding="utf-8"))
            )
        undeclared_contracts = linked_contracts - set(record["contracts"])
        for contract_id in sorted(undeclared_contracts):
            errors.append(f"{location}: linked local contract '{contract_id}' is not declared")

        expected_capabilities = {
            "goalpro_handoff": "handoff" in record["evals"],
            "quality_report": "quality" in record["evals"],
            "product_research": "product" in record["evals"],
        }
        for capability, expected in expected_capabilities.items():
            if record["capabilities"][capability] != expected:
                errors.append(f"{location}: capability '{capability}' disagrees with eval applicability")

        declared_test_paths = {
            token
            for command in record["tests"]
            for token in _declared_command_paths(command)
        }
        actual_test_paths = _skill_test_paths(repo_root, skill_path)
        for test_path in sorted(actual_test_paths - declared_test_paths):
            errors.append(f"{location}: skill-local test is not declared: {test_path}")
        for test_path in sorted(declared_test_paths):
            pure = Path(test_path)
            if pure.is_absolute() or ".." in pure.parts:
                errors.append(f"{location}: test command path must be repository-relative: {test_path}")
            elif not (repo_root / pure).is_file():
                errors.append(f"{location}: declared test path is missing: {test_path}")

        if record["maturity"] == "promoted" and not all(record["distribution"].values()):
            errors.append(f"{location}: promoted skills must remain in every stable distribution")

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args(argv)
    repo_root = args.repo_root.resolve()
    try:
        registry = load_registry(repo_root)
    except RegistryError as error:
        print(str(error), file=sys.stderr)
        return 1
    errors = validate_registry(repo_root, registry)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Registry validation failed: {len(errors)} error(s).", file=sys.stderr)
        return 1
    print(f"Validated registry schema and source coverage for {len(registry.records)} skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
