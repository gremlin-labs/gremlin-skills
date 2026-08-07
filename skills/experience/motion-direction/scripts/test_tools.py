#!/usr/bin/env python3
"""Unit tests for Motion Direction deterministic validators."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from validate_motion_direction_preview import REQUIRED_CATEGORIES, validate as validate_preview
from validate_motion_policy import CATEGORIES, POLICY_HEADINGS, validate as validate_policy


def preview_html() -> str:
    categories = "".join(
        f'<article data-motion-category="{category}" data-evidence-status="SIMULATED"><span>SIMULATED</span></article>'
        for category in sorted(REQUIRED_CATEGORIES)
    )
    return f"""<!doctype html><html lang="en" data-slug="joyful-console" data-revision="R1" data-evidence-timestamp="2026-08-06">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Motion Direction Studio</title></head>
<body><main><p>Planning preview, not production.</p>
<button data-direction-target="a" aria-controls="direction-a" aria-selected="true">Direction A</button>
<button data-direction-target="b" aria-controls="direction-b" aria-selected="false">Direction B</button>
<section id="direction-a" data-direction-panel="a">{categories}</section>
<section id="direction-b" data-direction-panel="b">Direction B comparison</section>
<button data-surface-target="home" aria-controls="surface-home" aria-selected="true">Home</button>
<button data-surface-target="queue" aria-controls="surface-queue" aria-selected="false">Queue</button>
<section id="surface-home" data-surface-panel="home">Home surface</section>
<section id="surface-queue" data-surface-panel="queue">Queue surface</section>
<button data-replay-motion>Replay</button><button data-motion-mode="full">Full motion</button>
<button data-motion-mode="reduced">Reduced motion</button><button data-stress-motion>Stress interruptions</button>
<button data-feedback-action="refine">REFINE</button><button data-feedback-action="new-set">NEW SET</button>
<button data-feedback-action="approve">APPROVE</button></main>
<style>@media (max-width: 40rem){{main{{display:block}}}} @media (prefers-reduced-motion: reduce){{*{{animation:none}}}}</style>
</body></html>"""


def policy_markdown() -> str:
    headings = "\n".join(f"## {heading.title()}\nConcrete TurbulenceJS guidance for reduced motion, interruption, cleanup, exception handling, rollout, and rollback.\n" for heading in sorted(POLICY_HEADINGS))
    return f"# Animation policy\n\n{headings}\n### ESSENTIAL\nFrequent.\n### EXPRESSIVE\nOccasional.\n### SIGNATURE\nRare.\n"


def matrix_markdown() -> str:
    rows = "\n".join(f"| `{category}` | APPLICABLE | Purpose |" for category in sorted(CATEGORIES))
    return f"# Component motion matrix\n\n| Category | Status | Purpose |\n| --- | --- | --- |\n{rows}\n"


class PreviewValidationTests(unittest.TestCase):
    def test_accepts_complete_self_contained_studio(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "preview.html"
            path.write_text(preview_html(), encoding="utf-8")
            self.assertEqual(validate_preview(path), [])

    def test_rejects_remote_content_and_missing_stress_control(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "preview.html"
            invalid = preview_html().replace("<button data-stress-motion>Stress interruptions</button>", "")
            invalid = invalid.replace("</head>", '<script src="https://example.com/motion.js"></script></head>')
            path.write_text(invalid, encoding="utf-8")
            errors = validate_preview(path)
            self.assertTrue(any("stress" in error for error in errors))
            self.assertTrue(any("remote" in error for error in errors))


class PolicyValidationTests(unittest.TestCase):
    def test_accepts_complete_policy_and_matrix(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            policy = Path(directory) / "ANIMATION-POLICY.md"
            matrix = Path(directory) / "COMPONENT-MOTION-MATRIX.md"
            policy.write_text(policy_markdown(), encoding="utf-8")
            matrix.write_text(matrix_markdown(), encoding="utf-8")
            self.assertEqual(validate_policy(policy, matrix), [])

    def test_rejects_placeholder_and_missing_category(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            policy = Path(directory) / "ANIMATION-POLICY.md"
            matrix = Path(directory) / "COMPONENT-MOTION-MATRIX.md"
            policy.write_text(policy_markdown() + "\n{unresolved}\n", encoding="utf-8")
            matrix.write_text(matrix_markdown().replace("| `spinner` | APPLICABLE | Purpose |\n", ""), encoding="utf-8")
            errors = validate_policy(policy, matrix)
            self.assertTrue(any("placeholder" in error for error in errors))
            self.assertTrue(any("spinner" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
