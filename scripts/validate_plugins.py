#!/usr/bin/env python3
"""Validate flat, host-specific Gremlin plugin payloads against source and registry."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from generate_plugin_manifests import (
    DEFAULT_OUTPUT,
    claude_skill_markdown,
    check_openai_metadata,
    package_metadata,
    plugin_manifest,
)
from package_skills import PackagingError, included_files
from skill_registry import RegistryError, load_registry


def _payload_files(root: Path) -> dict[Path, bytes]:
    return {
        path.relative_to(root): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def validate_plugins(repo_root: Path, output_root: Path) -> tuple[int, list[str]]:
    repo_root = repo_root.resolve()
    output_root = output_root.resolve()
    errors: list[str] = []
    try:
        registry = load_registry(repo_root)
        package = package_metadata(repo_root)
    except (RegistryError, OSError, ValueError) as error:
        return 0, [str(error)]
    errors.extend(check_openai_metadata(registry))
    expected_names = {record["name"] for record in registry.promoted}
    for host, manifest_dir in (("codex", ".codex-plugin"), ("claude", ".claude-plugin")):
        root = output_root / host / "gremlin-skills"
        manifest_path = root / manifest_dir / "plugin.json"
        try:
            actual_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            errors.append(f"{manifest_path}: {error}")
            continue
        if actual_manifest != plugin_manifest(host, package):
            errors.append(f"{manifest_path}: generated plugin manifest drift")
        skill_root = root / "skills"
        actual_names = {path.name for path in skill_root.iterdir() if path.is_dir()} if skill_root.is_dir() else set()
        if actual_names != expected_names:
            errors.append(
                f"{skill_root}: flat skill inventory mismatch; expected {len(expected_names)}, found {len(actual_names)}"
            )
        for record in registry.promoted:
            source = registry.skill_path(record)
            staged = skill_root / record["name"]
            if not staged.is_dir():
                continue
            try:
                expected = {
                    path.relative_to(source): path.read_bytes()
                    for path in included_files(source)
                }
            except PackagingError as error:
                errors.append(str(error))
                continue
            if host == "claude":
                skill_md = Path("SKILL.md")
                expected[skill_md] = claude_skill_markdown(
                    expected[skill_md].decode("utf-8"), record["invocation"]["claude"]
                ).encode("utf-8")
            actual = _payload_files(staged)
            if set(actual) != set(expected):
                errors.append(f"{staged}: staged files differ from source inventory")
                continue
            for relative in sorted(expected):
                if actual[relative] != expected[relative]:
                    errors.append(f"{staged / relative}: unexpected host transformation or source drift")
        if any(path.is_symlink() for path in root.rglob("*")):
            errors.append(f"{root}: plugin payload must not contain symlinks")
    receipt = output_root / "manifest.json"
    try:
        receipt_data = json.loads(receipt.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"{receipt}: {error}")
    else:
        if receipt_data.get("version") != package["version"] or len(receipt_data.get("hosts", [])) != 2:
            errors.append(f"{receipt}: plugin receipt identity mismatch")
    return len(expected_names), errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    repo_root = args.repo_root.resolve()
    output = (args.output or repo_root / DEFAULT_OUTPUT).resolve()
    count, errors = validate_plugins(repo_root, output)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Plugin validation failed: {len(errors)} error(s).", file=sys.stderr)
        return 1
    print(f"Validated flat Codex and Claude plugin payloads for {count} promoted skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
