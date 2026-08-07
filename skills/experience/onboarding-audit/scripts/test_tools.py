#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("validate_direction_input.py")
SPEC = importlib.util.spec_from_file_location("validate_direction_input", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


VALID = """# Onboarding direction input

## Source audit

See `RESEARCH.md`, `CURRENT-JOURNEY.md`, and `AUDIT-REPORT.md` for current evidence.

## Product promise and activation

The product promises a completed draft. Activation is the first saved draft.

## Platforms and segments

Platform classification: CROSS-PLATFORM

New individual creators are primary. Invited collaborators are secondary.

## Current journey

Users authenticate, answer one goal question, create a draft, and save it.

The current error and resume paths are documented in the journey artifact.

## Strengths to preserve

The starter prompt uses established product language and survives refresh.

## Prioritized findings

ONB-001 identifies an unrelated profile gate before draft creation.

## Constraints and non-goals

Authorization remains required before server-side generation. Billing is unchanged.

## Measurement and evidence gaps

The save event exists, but its relationship to retained use is not yet measured.

## Required direction outcomes

Every option must preserve authorization while reducing unrelated setup.

## Unknowns and experiments

Compare profile completion before and after first save behind an existing flag.

## Handoff state

READY

Direction can proceed from the verified current journey and named measurement gap.
"""


class DirectionInputTests(unittest.TestCase):
    def test_valid_handoff(self) -> None:
        self.assertEqual([], MODULE.validate_text(VALID))

    def test_missing_heading_and_sources(self) -> None:
        errors = MODULE.validate_text("# Onboarding direction input\n\nREADY\n")
        self.assertTrue(any("Product promise" in error for error in errors))
        self.assertTrue(any("RESEARCH.md" in error for error in errors))

    def test_rejects_multiple_classifications_and_placeholders(self) -> None:
        invalid = VALID.replace("CROSS-PLATFORM", "WEB and MOBILE").replace("READY", "READY\n\nTBD")
        errors = MODULE.validate_text(invalid)
        self.assertTrue(any("platform classification" in error for error in errors))
        self.assertTrue(any("placeholder" in error for error in errors))

    def test_prioritized_findings_require_stable_onboarding_ids(self) -> None:
        invalid = VALID.replace("ONB-001 identifies", "The audit identifies")
        errors = MODULE.validate_text(invalid)
        self.assertTrue(any("ONB-" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
