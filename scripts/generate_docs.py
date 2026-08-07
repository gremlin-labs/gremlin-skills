#!/usr/bin/env python3
"""Generate registry-owned documentation sections without rewriting curated prose."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Callable

from skill_registry import RegistryError, SkillRegistry, load_registry


BLOCKS = {
    "skill-index": ("<!-- BEGIN GENERATED:SKILL-INDEX -->", "<!-- END GENERATED:SKILL-INDEX -->"),
    "agent-pointers": ("<!-- BEGIN GENERATED:AGENT-POINTERS -->", "<!-- END GENERATED:AGENT-POINTERS -->"),
    "registry-contract": ("<!-- BEGIN GENERATED:REGISTRY-CONTRACT -->", "<!-- END GENERATED:REGISTRY-CONTRACT -->"),
}
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


class DocsGenerationError(RuntimeError):
    """Raised when a curated document is missing an owned block or source."""


def replace_block(text: str, block_name: str, content: str) -> str:
    begin, end = BLOCKS[block_name]
    if text.count(begin) != 1 or text.count(end) != 1:
        raise DocsGenerationError(f"expected exactly one {block_name} block")
    start = text.index(begin) + len(begin)
    finish = text.index(end, start)
    normalized = content.rstrip()
    return text[:start] + "\n" + normalized + "\n" + text[finish:]


def replace_heading_section(text: str, start_heading: str, end_heading: str, content: str) -> str:
    """Replace content between two unique level-two headings without HTML markers."""

    start_marker = f"{start_heading}\n"
    end_marker = f"\n{end_heading}\n"
    if text.count(start_marker) != 1 or text.count(end_marker) != 1:
        raise DocsGenerationError(f"expected exactly one {start_heading} to {end_heading} section")
    start = text.index(start_marker) + len(start_marker)
    finish = text.index(end_marker, start)
    return text[:start] + "\n" + content.rstrip() + "\n" + text[finish:]


def _frontmatter_description(skill_path: Path) -> str:
    text = (skill_path / "SKILL.md").read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise DocsGenerationError(f"{skill_path / 'SKILL.md'}: missing frontmatter")
    for line in match.group(1).splitlines():
        if line.startswith("description:"):
            return line.split(":", 1)[1].strip()
    raise DocsGenerationError(f"{skill_path / 'SKILL.md'}: missing description")


def _purpose(registry: SkillRegistry, record: dict[str, object]) -> str:
    description = _frontmatter_description(registry.skill_path(record))
    return description.split(" Use when ", 1)[0].strip()


def _escape_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_skill_index(registry: SkillRegistry, *, from_docs_index: bool = False) -> str:
    sections: list[str] = []
    for category in registry.data["category_model"]["values"]:
        sections.extend([
            f"### {category.title()}",
            "",
            "| Skill | Purpose | Authority |",
            "|---|---|---|",
        ])
        for record in registry.records:
            if record["category"] != category or record["maturity"] != "promoted":
                continue
            docs_path = Path(record["public_docs"]["path"])
            target = docs_path.name if from_docs_index else docs_path.as_posix()
            sections.append(
                f"| [{record['name']}]({target}) | {_escape_cell(_purpose(registry, record))} | "
                f"{record['authority']['mode']} |"
            )
        sections.append("")
    return "\n".join(sections).rstrip()


def render_readme_skill_table(registry: SkillRegistry) -> str:
    lines = [
        "| Skill | Description |",
        "|---|---|",
    ]
    for record in registry.promoted:
        lines.append(
            f"| [{record['name']}]({record['public_docs']['path']}) | "
            f"{_escape_cell(_purpose(registry, record))} |"
        )
    lines.extend([
        "",
        "The [full skill catalog](docs/skills/README.md) adds categories, authority, prerequisites, outputs, "
        "visible success, and adjacent workflows.",
    ])
    return "\n".join(lines)


def render_agent_pointers(registry: SkillRegistry) -> str:
    lines = [
        "| Skill | Category | Authority | Output root | Human docs |",
        "|---|---|---|---|---|",
    ]
    for record in registry.records:
        lines.append(
            f"| `{record['name']}` | {record['category']} | {record['authority']['mode']} | "
            f"`{record['output_root']}` | [{record['public_docs']['path']}]({record['public_docs']['path']}) |"
        )
    return "\n".join(lines)


def render_registry_contract(record: dict[str, object]) -> str:
    required = ", ".join(f"`{item}`" for item in record["dependencies"]["required_skills"]) or "None"
    optional = ", ".join(f"`{item}`" for item in record["dependencies"]["optional_skills"]) or "None"
    tests = "<br>".join(f"`{command}`" for command in record["tests"]) or "No skill-local suite declared"
    distribution = ", ".join(key for key, enabled in record["distribution"].items() if enabled) or "None"
    return "\n".join([
        "| Field | Registry value |",
        "|---|---|",
        f"| Category | `{record['category']}` ({record['maturity']}) |",
        f"| Invocation | `{record['invocation']['mode']}` |",
        f"| Authority | `{record['authority']['mode']}`; source mutation `{record['authority']['source_mutation']}`; external actions `{record['authority']['external_actions']}` |",
        f"| Output root | `{record['output_root']}` |",
        f"| Required skills | {required} |",
        f"| Optional skills | {optional} |",
        f"| Evaluation families | {', '.join(f'`{item}`' for item in record['evals'])} |",
        f"| Skill-local tests | {tests} |",
        f"| Stable distributions | {distribution} |",
    ])


def _updated(path: Path, block_name: str, content: str) -> str:
    if not path.is_file():
        raise DocsGenerationError(f"missing curated document: {path}")
    try:
        return replace_block(path.read_text(encoding="utf-8"), block_name, content)
    except DocsGenerationError as error:
        raise DocsGenerationError(f"{path}: {error}") from error


def collect_updates(repo_root: Path, registry: SkillRegistry | None = None) -> dict[Path, str]:
    repo_root = repo_root.resolve()
    registry = registry or load_registry(repo_root)
    readme_path = repo_root / "README.md"
    if not readme_path.is_file():
        raise DocsGenerationError(f"missing curated document: {readme_path}")
    try:
        readme = replace_heading_section(
            readme_path.read_text(encoding="utf-8"),
            "## Catalog",
            "## Lifecycle and composition",
            render_readme_skill_table(registry),
        )
    except DocsGenerationError as error:
        raise DocsGenerationError(f"{readme_path}: {error}") from error
    updates = {
        readme_path: readme,
        repo_root / "AGENTS.md": _updated(repo_root / "AGENTS.md", "agent-pointers", render_agent_pointers(registry)),
        repo_root / "docs" / "skills" / "README.md": _updated(
            repo_root / "docs" / "skills" / "README.md",
            "skill-index",
            render_skill_index(registry, from_docs_index=True),
        ),
    }
    for record in registry.promoted:
        path = repo_root / record["public_docs"]["path"]
        updates[path] = _updated(path, "registry-contract", render_registry_contract(record))
    return updates


def write_updates(updates: dict[Path, str]) -> None:
    for path, content in updates.items():
        temporary = path.with_name(f".{path.name}.tmp")
        temporary.write_text(content, encoding="utf-8")
        temporary.replace(path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--write", action="store_true", help="Rewrite only generated sections atomically.")
    args = parser.parse_args(argv)
    try:
        updates = collect_updates(args.repo_root)
    except (DocsGenerationError, RegistryError, OSError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    stale = [path for path, content in updates.items() if path.read_text(encoding="utf-8") != content]
    if args.write:
        write_updates({path: updates[path] for path in stale})
        print(f"Updated {len(stale)} generated documentation block(s).")
        return 0
    if stale:
        for path in stale:
            print(f"STALE: {path.relative_to(args.repo_root.resolve())}", file=sys.stderr)
        print("Run `python3 scripts/generate_docs.py --write`.", file=sys.stderr)
        return 1
    print(f"Validated generated documentation sections across {len(updates)} files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
