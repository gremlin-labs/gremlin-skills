#!/usr/bin/env python3
"""Validate the canonical Email Lifecycle Audit to Strategy handoff."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_HEADINGS = (
    "# Email lifecycle strategy input",
    "## Source audit",
    "## Product promise and lifecycle outcomes",
    "## Segments and maturity states",
    "## Current system",
    "## Strengths to preserve",
    "## Prioritized findings",
    "## Campaign and orchestration constraints",
    "## Consent deliverability and operational guardrails",
    "## Measurement and evidence gaps",
    "## Required strategy outcomes",
    "## Unknowns and experiments",
    "## Handoff authority",
    "## Handoff state",
)

STATES = ("READY", "PARTIAL", "BLOCKED")
SOURCE_LINKS = ("RESEARCH.md", "CURRENT-SYSTEM.md", "CAMPAIGN-INVENTORY.md", "AUDIT-REPORT.md")
FINDING_RE = re.compile(r"\bEML-\d{3}\b")
STRENGTH_RE = re.compile(r"\bEMS-\d{3}\b")
AUTHORITY_MARKER = "EVIDENCE_ONLY"
PLACEHOLDER_RE = re.compile(r"\b(?:TODO|FIXME|TBD)\b|\{(?:insert|replace|example)[^}]*\}", re.IGNORECASE)


def _section(text: str, heading: str, next_heading: str) -> str:
    start = text.find(heading)
    end = text.find(next_heading)
    if start < 0 or end < 0 or end <= start:
        return ""
    return text[start + len(heading):end]


def validate_text(text: str, audit_text: str | None = None) -> list[str]:
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

    state_matches = [
        state
        for state in STATES
        if re.search(rf"(?m)^\s*(?:[-*]\s*)?(?:State:\s*)?{state}\s*$", text)
    ]
    if len(state_matches) != 1:
        errors.append("expected exactly one standalone handoff state: READY, PARTIAL, or BLOCKED")

    for source in SOURCE_LINKS:
        if source not in text:
            errors.append(f"missing required source link: {source}")

    strength_section = _section(text, "## Strengths to preserve", "## Prioritized findings")
    finding_section = _section(text, "## Prioritized findings", "## Campaign and orchestration constraints")

    if not STRENGTH_RE.search(strength_section):
        errors.append("missing stable EMS-000 strength reference in Strengths to preserve")

    if not FINDING_RE.search(finding_section):
        errors.append("missing stable EML-000 finding reference in Prioritized findings")

    authority_matches = re.findall(rf"(?m)^\s*{AUTHORITY_MARKER}\s*$", text)
    if len(authority_matches) != 1:
        errors.append(f"expected exactly one standalone handoff authority marker: {AUTHORITY_MARKER}")

    if audit_text is not None:
        audit_findings = set(FINDING_RE.findall(audit_text))
        audit_strengths = set(STRENGTH_RE.findall(audit_text))
        handoff_findings = set(FINDING_RE.findall(finding_section))
        handoff_strengths = set(STRENGTH_RE.findall(strength_section))

        if not audit_findings:
            errors.append("AUDIT-REPORT.md contains no stable EML-000 finding IDs")
        if not audit_strengths:
            errors.append("AUDIT-REPORT.md contains no stable EMS-000 strength IDs")

        missing_findings = sorted(audit_findings - handoff_findings)
        missing_strengths = sorted(audit_strengths - handoff_strengths)
        if missing_findings:
            errors.append("handoff omits audit findings: " + ", ".join(missing_findings))
        if missing_strengths:
            errors.append("handoff omits audit strengths: " + ", ".join(missing_strengths))

    if PLACEHOLDER_RE.search(text):
        errors.append("unresolved placeholder marker found")

    if len(text.strip().splitlines()) < 42:
        errors.append("handoff is too short to contain usable evidence")

    return errors


def validate_path(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    audit_path = path.with_name("AUDIT-REPORT.md")
    audit_text = audit_path.read_text(encoding="utf-8") if audit_path.is_file() else None
    errors = validate_text(text, audit_text)

    for source in SOURCE_LINKS:
        if not path.with_name(source).is_file():
            errors.append(f"missing required source artifact beside handoff: {source}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    args = parser.parse_args()

    if not args.path.is_file():
        print(f"ERROR: file not found: {args.path}", file=sys.stderr)
        return 1

    errors = validate_path(args.path)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"Validated email lifecycle strategy input: {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
