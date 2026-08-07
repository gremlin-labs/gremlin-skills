#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("validate_onboarding_preview.py")
SPEC = importlib.util.spec_from_file_location("validate_onboarding_preview", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def panel(option: str) -> str:
    sections = "".join(
        f'<section data-preview-section="{name}">{name}</section>'
        for name in MODULE.REQUIRED_SECTIONS
    )
    return f'''<article id="{option}" data-direction-panel="{option}">
      {sections}
      <div data-platform-view="web">
        <button data-flow-step="1">Choose a goal</button>
        <button data-flow-step="2" data-activation-moment="true">Save the first draft</button>
      </div>
    </article>'''


VALID = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Onboarding comparison</title>
  <style>
    button:focus-visible {{ outline: 2px solid blue; }}
    @media (max-width: 40rem) {{ main {{ display: block; }} }}
    @media (prefers-reduced-motion: reduce) {{ * {{ animation-duration: 0.01ms; }} }}
  </style>
</head>
<body data-onboarding-preview="true" data-preview-revision="R1"
      data-onboarding-slug="first-draft" data-evidence-date="2026-08-06"
      data-platform-scope="web">
  <header>Planning preview, not production.</header>
  <nav aria-label="Directions">
    <button data-direction-target="a" aria-controls="a" aria-selected="true">A</button>
    <button data-direction-target="b" aria-controls="b" aria-selected="false">B</button>
  </nav>
  <main>
    {panel("a")}
    {panel("b")}
  </main>
  <aside>
    <button data-preview-action="refine">Refine</button>
    <button data-preview-action="new-set">New set</button>
    <button data-preview-action="approve">Approve</button>
  </aside>
  <script>document.documentElement.dataset.previewReady = "true";</script>
</body>
</html>'''


class PreviewValidatorTests(unittest.TestCase):
    def test_valid_preview(self) -> None:
        self.assertEqual([], MODULE.validate_text(VALID))

    def test_missing_sections_and_actions(self) -> None:
        invalid = VALID.replace('data-preview-section="measurement"', 'data-preview-section="missing"')
        invalid = invalid.replace('data-preview-action="approve"', 'data-preview-action="missing"')
        errors = MODULE.validate_text(invalid)
        self.assertTrue(any("measurement" in error for error in errors))
        self.assertTrue(any("approve" in error for error in errors))

    def test_aria_controls_must_reference_the_matching_panel_id(self) -> None:
        invalid = VALID.replace('aria-controls="a"', 'aria-controls="missing"', 1)
        errors = MODULE.validate_text(invalid)
        self.assertTrue(any("aria-controls" in error for error in errors))

    def test_rejects_remote_and_placeholder_content(self) -> None:
        invalid = VALID.replace("</main>", '<img src="https://example.com/image.png" alt="Acme">\n</main>')
        errors = MODULE.validate_text(invalid)
        self.assertTrue(any("remote" in error for error in errors))
        self.assertTrue(any("placeholder" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
