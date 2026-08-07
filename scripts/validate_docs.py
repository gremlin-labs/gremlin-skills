#!/usr/bin/env python3
"""Validate curated human docs, generated registry blocks, links, and credits."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from generate_docs import DocsGenerationError, collect_updates
from skill_registry import RegistryError, SkillRegistry, load_registry


HEADER_IMAGE = "![Gremlin Skills: A Very Particular Set of Skills](assets/gremlinlabs-gremlin-skills.jpg)"
TAKEN_PREAMBLE_MARKERS = (
    "a very particular set of agent skills",
    "nightmare for your competitors",
)
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
REQUIRED_HUMAN_HEADINGS = {
    "When to reach for it",
    "Prerequisites",
    "Authority and safety",
    "Outputs",
    "Common questions",
    "Visible success",
    "Adjacent Gremlin skills",
    "Registry contract",
}


def _headings(path: Path) -> set[str]:
    return {
        line.lstrip("#").strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.startswith("#")
    }


def _validate_links(paths: list[Path]) -> list[str]:
    errors: list[str] = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for match in LINK_RE.finditer(text):
            raw = match.group(1).strip().split(maxsplit=1)[0].strip("<>")
            target = raw.split("#", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                line = text.count("\n", 0, match.start()) + 1
                errors.append(f"{path}:{line}: broken local link '{raw}'")
    return errors


def validate_docs(repo_root: Path, registry: SkillRegistry | None = None) -> list[str]:
    repo_root = repo_root.resolve()
    errors: list[str] = []
    if registry is None:
        try:
            registry = load_registry(repo_root)
        except RegistryError as error:
            return str(error).splitlines()

    readme = repo_root / "README.md"
    acknowledgements = repo_root / "ACKNOWLEDGEMENTS.md"
    notices = repo_root / "THIRD-PARTY-NOTICES.md"
    required_roots = [
        readme,
        repo_root / "CHANGELOG.md",
        repo_root / "LICENSE",
        repo_root / "CONTRIBUTING.md",
        repo_root / "SECURITY.md",
        repo_root / "AGENTS.md",
        repo_root / "CONTEXT.md",
        acknowledgements,
        notices,
        repo_root / "docs" / "architecture" / "invocation.md",
        repo_root / "docs" / "architecture" / "lifecycle.md",
        repo_root / "docs" / "architecture" / "packaging.md",
        repo_root / "docs" / "maintaining-skills.md",
        repo_root / "docs" / "incubator.md",
        repo_root / "docs" / "adr" / "0001-registry-as-package-api.md",
        repo_root / "docs" / "adr" / "0002-independent-coexistence.md",
        repo_root / "docs" / "skills" / "README.md",
    ]
    for path in required_roots:
        if not path.is_file():
            errors.append(f"missing public document: {path.relative_to(repo_root)}")

    public_pages: list[Path] = []
    for record in registry.promoted:
        docs = record["public_docs"]
        path = repo_root / docs["path"]
        public_pages.append(path)
        if docs["status"] != "published":
            errors.append(f"registry skill '{record['name']}': promoted human doc is not published")
            continue
        if not path.is_file():
            errors.append(f"registry skill '{record['name']}': missing human doc {docs['path']}")
            continue
        missing = sorted(REQUIRED_HUMAN_HEADINGS - _headings(path))
        if missing:
            errors.append(f"{docs['path']}: missing heading(s): {', '.join(missing)}")

    if readme.is_file():
        readme_text = readme.read_text(encoding="utf-8")
        if HEADER_IMAGE not in readme_text:
            errors.append("README.md: missing Gremlin Skills header image")
        if "<!-- BEGIN GENERATED:" in readme_text or "<!-- END GENERATED:" in readme_text:
            errors.append("README.md: generated HTML comment markers belong only in internal documentation")
        for marker in TAKEN_PREAMBLE_MARKERS:
            if marker not in readme_text.lower():
                errors.append(f"README.md: missing opening preamble marker '{marker}'")
        if readme_text.count("[acknowledgements](ACKNOWLEDGEMENTS.md)") != 1:
            errors.append("README.md: expected one concise acknowledgements link")
        if len(readme_text.splitlines()) > 300:
            errors.append("README.md: public entrypoint exceeds 300 lines; move detail into human docs")

    if acknowledgements.is_file():
        text = acknowledgements.read_text(encoding="utf-8")
        for phrase in ("# Acknowledgements", "independently authored", "does not imply endorsement"):
            if phrase not in text:
                errors.append(f"ACKNOWLEDGEMENTS.md: missing required statement containing '{phrase}'")

    if notices.is_file():
        notice_text = notices.read_text(encoding="utf-8")
        local_notices = sorted((repo_root / "skills").rglob("THIRD-PARTY-NOTICES.md"))
        for local_notice in local_notices:
            relative = local_notice.relative_to(repo_root).as_posix()
            if relative not in notice_text:
                errors.append(f"THIRD-PARTY-NOTICES.md: missing notice index entry for {relative}")

    existing_paths = [path for path in required_roots + public_pages if path.is_file()]
    errors.extend(_validate_links(existing_paths))

    try:
        updates = collect_updates(repo_root, registry)
    except (DocsGenerationError, RegistryError, OSError) as error:
        errors.append(str(error))
    else:
        for path, expected in updates.items():
            if path.read_text(encoding="utf-8") != expected:
                errors.append(f"{path.relative_to(repo_root)}: generated registry block is stale")
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
    errors = validate_docs(repo_root, registry)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Documentation validation failed: {len(errors)} error(s).", file=sys.stderr)
        return 1
    print(f"Validated public documentation for {len(registry.promoted)} promoted skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
