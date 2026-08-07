#!/usr/bin/env python3
"""Validate Motion Direction animation-policy and component-matrix coverage."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


POLICY_HEADINGS = {
    "principles and emotional intent",
    "spatial model and rhythm",
    "delight tiers",
    "semantic roles and tokens",
    "page and component recipes",
    "interruption and lifecycle",
    "reduced motion and input",
    "performance and resource budgets",
    "prohibited patterns",
    "exceptions",
    "new-component decision tree",
    "agent and contributor guidance",
    "enforcement and verification",
    "rollout and rollback",
    "approval",
}
CATEGORIES = {
    "page-load",
    "route-transition",
    "navigation",
    "menu",
    "sidebar-drawer",
    "overlay-dialog",
    "tooltip-popover",
    "tabs-accordion",
    "controls",
    "form-validation",
    "list-table-card",
    "direct-manipulation",
    "skeleton",
    "spinner",
    "loading-progress",
    "empty-error-recovery",
    "toast-notification",
    "onboarding-celebration",
}
VALID_STATUSES = {"APPLICABLE", "NOT APPLICABLE", "UNVERIFIED"}
PLACEHOLDER = re.compile(r"\{[^}\n]+\}|\b(?:TODO|FIXME|TBD)\b", re.IGNORECASE)


def _headings(text: str) -> set[str]:
    return {
        match.group(1).strip().lower()
        for match in re.finditer(r"^#{2,6}\s+(.+?)\s*$", text, re.MULTILINE)
    }


def validate(policy_path: Path, matrix_path: Path) -> list[str]:
    policy = policy_path.read_text(encoding="utf-8")
    matrix = matrix_path.read_text(encoding="utf-8")
    errors: list[str] = []

    missing_headings = sorted(POLICY_HEADINGS - _headings(policy))
    if missing_headings:
        errors.append(f"animation policy is missing headings: {', '.join(missing_headings)}")
    for term in ("ESSENTIAL", "EXPRESSIVE", "SIGNATURE", "TurbulenceJS"):
        if term not in policy:
            errors.append(f"animation policy is missing required term: {term}")
    for concept in ("reduced", "interruption", "cleanup", "exception", "rollout", "rollback"):
        if not re.search(rf"\b{re.escape(concept)}\w*\b", policy, re.IGNORECASE):
            errors.append(f"animation policy is missing {concept} guidance")

    found_categories: dict[str, list[str]] = {}
    for line in matrix.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        category = cells[0].strip("`")
        if category in CATEGORIES:
            found_categories.setdefault(category, []).append(cells[1])
    missing_categories = sorted(CATEGORIES - set(found_categories))
    if missing_categories:
        errors.append(f"component matrix is missing categories: {', '.join(missing_categories)}")
    duplicates = sorted(category for category, statuses in found_categories.items() if len(statuses) != 1)
    if duplicates:
        errors.append(f"component matrix categories must appear exactly once: {', '.join(duplicates)}")
    invalid = sorted(
        f"{category}={statuses[0]}"
        for category, statuses in found_categories.items()
        if statuses and statuses[0] not in VALID_STATUSES
    )
    if invalid:
        errors.append(f"component matrix has invalid dispositions: {', '.join(invalid)}")
    if PLACEHOLDER.search(policy) or PLACEHOLDER.search(matrix):
        errors.append("policy and matrix must not contain unresolved placeholders")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("policy", type=Path)
    parser.add_argument("matrix", type=Path)
    args = parser.parse_args()
    for path in (args.policy, args.matrix):
        if not path.is_file():
            parser.error(f"not a file: {path}")
    errors = validate(args.policy, args.matrix)
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        return 1
    print(f"Validated motion policy: {args.policy} + {args.matrix}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
