#!/usr/bin/env python3
"""Validate the canonical Onboarding Audit to Onboarding Direction handoff."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_HEADINGS = (
    "# Onboarding direction input",
    "## Source audit",
    "## Product promise and activation",
    "## Platforms and segments",
    "## Current journey",
    "## Strengths to preserve",
    "## Prioritized findings",
    "## Constraints and non-goals",
    "## Measurement and evidence gaps",
    "## Required direction outcomes",
    "## Unknowns and experiments",
    "## Handoff state",
)

PLATFORMS = ("WEB", "MOBILE", "CROSS-PLATFORM")
STATES = ("READY", "PARTIAL", "BLOCKED")
SOURCE_LINKS = ("RESEARCH.md", "CURRENT-JOURNEY.md", "AUDIT-REPORT.md")
PLACEHOLDER_RE = re.compile(r"\b(?:TODO|FIXME|TBD)\b|\{(?:insert|replace|example)[^}]*\}", re.IGNORECASE)


def validate_text(text: str) -> list[str]:
    errors: list[str] = []
    positions: list[int] = []

    for heading in REQUIRED_HEADINGS:
        count = text.count(heading)
        if count != 1:
            errors.append(f"expected exactly one heading: {heading}")
            positions.append(-1)
        else:
            positions.append(text.index(heading))

    present_positions = [position for position in positions if position >= 0]
    if present_positions != sorted(present_positions):
        errors.append("required headings are out of order")

    platform_matches = [platform for platform in PLATFORMS if re.search(rf"\b{re.escape(platform)}\b", text)]
    if len(platform_matches) != 1:
        errors.append("expected exactly one platform classification: WEB, MOBILE, or CROSS-PLATFORM")

    state_matches = [state for state in STATES if re.search(rf"(?m)^\s*(?:[-*]\s*)?(?:State:\s*)?{state}\s*$", text)]
    if len(state_matches) != 1:
        errors.append("expected exactly one standalone handoff state: READY, PARTIAL, or BLOCKED")

    for source in SOURCE_LINKS:
        if source not in text:
            errors.append(f"missing required source link: {source}")

    findings = re.search(
        r"(?ms)^## Prioritized findings\s*$\n(.*?)(?=^## |\Z)",
        text,
    )
    if not findings or not re.search(r"\bONB-\d{3,}\b", findings.group(1)):
        errors.append("Prioritized findings must preserve at least one stable ONB-{number} ID")

    if PLACEHOLDER_RE.search(text):
        errors.append("unresolved placeholder marker found")

    if len(text.strip().splitlines()) < 36:
        errors.append("handoff is too short to contain usable evidence")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    args = parser.parse_args()

    if not args.path.is_file():
        print(f"ERROR: file not found: {args.path}", file=sys.stderr)
        return 1

    errors = validate_text(args.path.read_text(encoding="utf-8"))
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"Validated onboarding direction input: {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
