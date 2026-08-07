#!/usr/bin/env python3
"""Unit tests for Design Direction preview validation."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from validate_direction_preview import validate


SECTIONS = "".join(f'<div data-preview-section="{section}"></div>' for section in sorted({
    "direction-summary", "typography", "palette", "surfaces", "components",
    "states", "responsive", "motion", "tradeoffs",
}))
VALID = f"""<!doctype html><html lang="en"><head><title>Directions</title><meta name="viewport" content="width=device-width"></head>
<body><main><button data-direction-target="a" aria-controls="panel-a" aria-selected="true"></button>
<button data-direction-target="b" aria-controls="panel-b" aria-selected="false"></button>
<section id="panel-a" data-direction-panel="a">{SECTIONS}</section><section id="panel-b" data-direction-panel="b">{SECTIONS}</section>
<button data-feedback-action="refine"></button>
<button data-feedback-action="new-set"></button><button data-feedback-action="approve"></button></main>
<style>@media (max-width: 40rem){{}} @media (prefers-reduced-motion: reduce){{}}</style></body></html>"""


class PreviewValidationTests(unittest.TestCase):
    def test_accepts_complete_self_contained_preview(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "preview.html"
            path.write_text(VALID, encoding="utf-8")
            self.assertEqual(validate(path), [])

    def test_rejects_remote_assets_and_placeholders(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "preview.html"
            path.write_text(VALID.replace("</head>", '<script src="https://example.com/x.js"></script></head>').replace("Directions", "TODO Directions"), encoding="utf-8")
            errors = validate(path)
            self.assertTrue(any("remote" in error for error in errors))
            self.assertTrue(any("placeholder" in error for error in errors))

    def test_requires_complete_sections_inside_every_direction(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "preview.html"
            path.write_text(VALID.replace(f'<section id="panel-b" data-direction-panel="b">{SECTIONS}</section>', '<section id="panel-b" data-direction-panel="b"></section>'), encoding="utf-8")
            errors = validate(path)
            self.assertTrue(any("panel-b is missing sections" in error for error in errors))
if __name__ == "__main__":
    unittest.main()
