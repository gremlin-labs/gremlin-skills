#!/usr/bin/env python3
"""Validate Gremlin skill structure, links, documentation, and installation sync."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from skill_registry import RegistryError, load_registry


NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
XML_PLACEHOLDER_RE = re.compile(r"<[a-zA-Z][a-zA-Z0-9-]*>")
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
PLACEHOLDER_RE = re.compile(r"\b(?:TODO|FIXME)\b")
LEGACY_ARTIFACT_RE = re.compile(
    r"(?<![\w-])(?:goals|plans|feature-specs|audits|proposals|migrations|"
    r"releases|restructures|brainstorms)/\{(?:slug|goal-slug|version)\}/"
)
THEME_LIBRARY_DISCOVERY = "## Optional shared Theme Library"
RUNTIME_EXCLUDED_NAMES = {".DS_Store", "__pycache__"}
RUNTIME_EXCLUDED_SUFFIXES = {".pyc", ".pyo"}


def _frontmatter(path: Path) -> tuple[dict[str, str], list[str]]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, [f"{path}: missing or malformed YAML frontmatter"]

    values: dict[str, str] = {}
    for number, raw_line in enumerate(match.group(1).splitlines(), start=2):
        line = raw_line.strip()
        if not line:
            continue
        if ":" not in line:
            errors.append(f"{path}:{number}: malformed frontmatter line")
            continue
        key, value = line.split(":", 1)
        key, value = key.strip(), value.strip()
        if key in values:
            errors.append(f"{path}:{number}: duplicate frontmatter key '{key}'")
        values[key] = value

    unexpected = sorted(set(values) - {"name", "description"})
    if unexpected:
        errors.append(f"{path}: unsupported frontmatter keys: {', '.join(unexpected)}")
    for required in ("name", "description"):
        if not values.get(required):
            errors.append(f"{path}: missing frontmatter field '{required}'")
    return values, errors


def _validate_markdown(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    for path in sorted(skill_dir.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        for match in XML_PLACEHOLDER_RE.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            errors.append(f"{path}:{line}: XML-like placeholder '{match.group(0)}'")
        for match in PLACEHOLDER_RE.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            errors.append(f"{path}:{line}: unresolved initializer marker '{match.group(0)}'")
        for match in LINK_RE.finditer(text):
            raw_target = match.group(1).strip().split(maxsplit=1)[0].strip("<>")
            target = raw_target.split("#", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            parts = Path(target).parts
            if parts.count("..") > 1 or (".." in parts and parts[0] != ".."):
                errors.append(f"{path}: reference is deeper than one sibling level: {raw_target}")
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                errors.append(f"{path}: broken relative link: {raw_target}")
    return errors


def _validate_openai_yaml(skill_dir: Path, name: str, invocation_mode: str) -> list[str]:
    path = skill_dir / "agents" / "openai.yaml"
    if not path.exists():
        return [f"{path}: missing generated Codex metadata"]
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    for key in ("display_name", "short_description", "default_prompt"):
        if not re.search(rf'^\s+{key}:\s+"[^"\n]+"\s*$', text, re.MULTILINE):
            errors.append(f"{path}: interface.{key} must be present and double-quoted")
    prompt = re.search(r'^\s+default_prompt:\s+"([^"\n]+)"\s*$', text, re.MULTILINE)
    if prompt and f"${name}" not in prompt.group(1):
        errors.append(f"{path}: default_prompt must mention '${name}'")
    summary = re.search(r'^\s+short_description:\s+"([^"\n]+)"\s*$', text, re.MULTILINE)
    if summary and not 25 <= len(summary.group(1)) <= 64:
        errors.append(f"{path}: interface.short_description must be 25-64 characters")
    policy = re.search(r'^\s+allow_implicit_invocation:\s+(true|false)\s*$', text, re.MULTILINE)
    if not policy:
        errors.append(f"{path}: policy.allow_implicit_invocation must be present and boolean")
    elif invocation_mode != "pending-owner-review":
        expected = invocation_mode == "model-visible"
        if (policy.group(1) == "true") != expected:
            errors.append(f"{path}: Codex implicit-invocation policy disagrees with registry mode '{invocation_mode}'")
    return errors


def validate_skill(skill_dir: Path, readme_text: str, record: dict[str, object]) -> list[str]:
    errors: list[str] = []
    skill_path = skill_dir / "SKILL.md"
    if not skill_path.exists():
        return [f"{skill_dir}: missing SKILL.md"]

    frontmatter, fm_errors = _frontmatter(skill_path)
    errors.extend(fm_errors)
    name = frontmatter.get("name", "")
    if name and not NAME_RE.fullmatch(name):
        errors.append(f"{skill_path}: name must be lowercase kebab-case")
    if name and name != skill_dir.name:
        errors.append(f"{skill_path}: name '{name}' does not match directory '{skill_dir.name}'")

    description = frontmatter.get("description", "")
    use_when = description.find("Use when")
    if use_when < 10:
        errors.append(f"{skill_path}: description needs a capability sentence followed by 'Use when'")

    skill_text = skill_path.read_text(encoding="utf-8")
    capabilities = record["capabilities"]
    if capabilities["decision_tree"] and "```dot" not in skill_text:
        errors.append(f"{skill_path}: missing fenced Graphviz decision tree")
    if capabilities["work_artifacts"] and "(contracts/work-artifacts.md)" not in skill_text:
        errors.append(f"{skill_path}: missing generated local work-artifact contract link")
    canonical_root = record["output_root"]
    if name and capabilities["work_artifacts"] and canonical_root not in skill_text:
        errors.append(f"{skill_path}: missing canonical output root '{canonical_root}'")
    if name and capabilities["theme_library_discovery"] and THEME_LIBRARY_DISCOVERY not in skill_text:
        errors.append(f"{skill_path}: missing independently installed Theme Library discovery contract")
    legacy = LEGACY_ARTIFACT_RE.search(skill_text)
    if legacy:
        errors.append(f"{skill_path}: declares legacy generated-work root '{legacy.group(0)}'")
    errors.extend(_validate_markdown(skill_dir))
    if name and capabilities["readme_registration"]:
        tree_pattern = re.compile(rf"[├└]──\s+{re.escape(name)}/")
        index_pattern = re.compile(rf"^###\s+{re.escape(name)}(?:\s|$)", re.MULTILINE)
        generated_index_pattern = re.compile(
            rf"\|\s+\[{re.escape(name)}\]\(docs/skills/{re.escape(name)}\.md\)\s+\|"
        )
        if not (
            tree_pattern.search(readme_text)
            or index_pattern.search(readme_text)
            or generated_index_pattern.search(readme_text)
        ):
            errors.append(f"README.md: skill '{name}' missing from catalog listing")
        errors.extend(_validate_openai_yaml(skill_dir, name, record["invocation"]["codex"]))
    return errors


def _file_map(directory: Path) -> dict[Path, bytes]:
    return {
        path.relative_to(directory): path.read_bytes()
        for path in sorted(directory.rglob("*"))
        if path.is_file()
        and not any(part in RUNTIME_EXCLUDED_NAMES for part in path.relative_to(directory).parts)
        and path.suffix not in RUNTIME_EXCLUDED_SUFFIXES
    }


def compare_installed(repo_skill: Path, global_root: Path, installed_name: str | None = None) -> list[str]:
    installed = global_root / (installed_name or repo_skill.name)
    if not installed.is_dir():
        return [f"{installed}: installed skill is missing"]
    repo_files = _file_map(repo_skill)
    installed_files = _file_map(installed)
    errors: list[str] = []
    for relative in sorted(repo_files.keys() - installed_files.keys()):
        errors.append(f"{installed}: missing installed file {relative}")
    for relative in sorted(installed_files.keys() - repo_files.keys()):
        errors.append(f"{installed}: extra installed file {relative}")
    for relative in sorted(repo_files.keys() & installed_files.keys()):
        if repo_files[relative] != installed_files[relative]:
            errors.append(f"{installed / relative}: differs from repository copy")
    return errors


def validate_repo(repo_root: Path, global_root: Path | None = None) -> tuple[list[str], list[str]]:
    skills_root = repo_root / "skills"
    readme = repo_root / "README.md"
    if not skills_root.is_dir() or not readme.is_file():
        return [], [f"{repo_root}: expected skills/ and README.md"]
    readme_text = readme.read_text(encoding="utf-8")
    try:
        registry = load_registry(repo_root)
    except RegistryError as error:
        return [], str(error).splitlines()
    errors: list[str] = []
    for record in registry.records:
        skill_dir = registry.skill_path(record)
        errors.extend(validate_skill(skill_dir, readme_text, record))
        if global_root is not None:
            errors.extend(compare_installed(skill_dir, global_root, record["name"]))
    return list(registry.names), errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--global-root", type=Path)
    args = parser.parse_args(argv)
    names, errors = validate_repo(args.repo_root.resolve(), args.global_root.expanduser().resolve() if args.global_root else None)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Validation failed: {len(errors)} error(s) across {len(names)} skill(s).", file=sys.stderr)
        return 1
    sync = " with installed copies synchronized" if args.global_root else ""
    print(f"Validated {len(names)} skills{sync}: {', '.join(names)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
