#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("validate_strategy_input.py")
SPEC = importlib.util.spec_from_file_location("validate_strategy_input", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


VALID = """# Email lifecycle strategy input

## Source audit

See `RESEARCH.md`, `CURRENT-SYSTEM.md`, `CAMPAIGN-INVENTORY.md`, and `AUDIT-REPORT.md`.

The audit used source and sanitized provider-preview evidence.

## Product promise and lifecycle outcomes

The product promises a published client brief. First value is the first published brief; second value is a reused brief workflow.

## Segments and maturity states

New individual consultants are primary. Team reviewers and returning paid users are secondary.

States cover unactivated, first value, repeated value, active, at risk, lapsed, reactivated, and suppressed.

## Current system

Product events enter one scheduler and two provider streams. Current exits are incomplete for the activation rescue path.

The system and data limits are detailed in the linked artifacts.

## Strengths to preserve

EMS-001 identifies isolated transactional verification.

EMS-002 identifies the welcome sender's monitored reply path.

## Prioritized findings

EML-001 identifies completed users who remain eligible for activation rescue.

EML-004 records an unverified consent mapping for imported team members.

## Campaign and orchestration constraints

Security and billing mail retain priority. The existing global frequency cap must remain conservative during migration.

## Consent deliverability and operational guardrails

Marketing suppression is durable. Imported-member eligibility requires qualified review before implementation.

Current SPF and DKIM evidence is verified; DMARC reporting ownership remains unclear.

## Measurement and evidence gaps

First-value completion is measured, but its relationship to retained use and incremental email lift is unknown.

## Required strategy outcomes

Every option must exit rescue immediately after first value and separate imported-member assumptions from approved eligibility.

## Unknowns and experiments

Run a holdout on one activation intervention and verify imported-member consent with the product and legal owners.

## Handoff authority

EVIDENCE_ONLY

This handoff records evidence and readiness. It does not authorize strategy, implementation, provider or DNS changes, deployment, or sending.

## Handoff state

PARTIAL

Strategy may proceed with the named consent limitation and validation experiment visible in every option.
"""

AUDIT = """# Email lifecycle audit report

## Verified strengths

### EMS-001 — Transactional verification is isolated

### EMS-002 — Welcome replies are monitored

## Prioritized findings

### EML-001 — Completed users remain eligible

### EML-004 — Imported-member consent is unverified
"""


class StrategyInputTests(unittest.TestCase):
    def test_valid_handoff(self) -> None:
        self.assertEqual([], MODULE.validate_text(VALID, AUDIT))

    def test_missing_heading_sources_and_finding(self) -> None:
        errors = MODULE.validate_text("# Email lifecycle strategy input\n\nREADY\n")
        self.assertTrue(any("Product promise" in error for error in errors))
        self.assertTrue(any("CAMPAIGN-INVENTORY.md" in error for error in errors))
        self.assertTrue(any("EML-000" in error for error in errors))
        self.assertTrue(any("EMS-000" in error for error in errors))
        self.assertTrue(any("EVIDENCE_ONLY" in error for error in errors))

    def test_rejects_multiple_states_and_placeholders(self) -> None:
        invalid = VALID.replace("PARTIAL", "PARTIAL\n\nREADY\n\nTBD")
        errors = MODULE.validate_text(invalid)
        self.assertTrue(any("handoff state" in error for error in errors))
        self.assertTrue(any("placeholder" in error for error in errors))

    def test_rejects_missing_audit_ids(self) -> None:
        audit = AUDIT + "\n### EMS-003 — Safe fallback exists\n\n### EML-009 — Rendering is unverified\n"
        errors = MODULE.validate_text(VALID, audit)
        self.assertTrue(any("EML-009" in error for error in errors))
        self.assertTrue(any("EMS-003" in error for error in errors))

    def test_rejects_authority_marker_as_permission(self) -> None:
        errors = MODULE.validate_text(VALID.replace("EVIDENCE_ONLY", "STRATEGY_AUTHORIZED"), AUDIT)
        self.assertTrue(any("EVIDENCE_ONLY" in error for error in errors))

    def test_path_validation_requires_linked_source_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            handoff = root / "STRATEGY-INPUT.md"
            handoff.write_text(VALID, encoding="utf-8")
            for source in MODULE.SOURCE_LINKS:
                content = AUDIT if source == "AUDIT-REPORT.md" else f"# {source}\n"
                (root / source).write_text(content, encoding="utf-8")

            self.assertEqual([], MODULE.validate_path(handoff))

            (root / "CAMPAIGN-INVENTORY.md").unlink()
            errors = MODULE.validate_path(handoff)
            self.assertTrue(any("CAMPAIGN-INVENTORY.md" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
