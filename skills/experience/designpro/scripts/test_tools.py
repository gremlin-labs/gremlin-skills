#!/usr/bin/env python3
"""Unit tests for Designpro's deterministic audit utilities."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import contrast_matrix
import design_value_inventory


class ContrastMatrixTests(unittest.TestCase):
    def test_black_on_white_passes(self) -> None:
        report = contrast_matrix.evaluate_model({
            "themes": {
                "light": {
                    "tokens": {"page": "#fff", "text": "#000"},
                    "pairs": [{
                        "name": "body",
                        "foreground": "text",
                        "background": ["page"],
                        "kind": "normal-text",
                    }],
                }
            }
        })
        self.assertEqual(report["summary"], {"pairs": 1, "passed": 1, "failed": 0})
        self.assertEqual(report["results"][0]["ratio"], 21.0)

    def test_alias_and_alpha_layers_are_composited(self) -> None:
        report = contrast_matrix.evaluate_model({
            "themes": {
                "dark": {
                    "tokens": {
                        "page": "#000",
                        "overlay": "rgba(255, 255, 255, 0.5)",
                        "surface": "$overlay",
                        "text": "#fff",
                    },
                    "pairs": [{
                        "name": "overlay text",
                        "foreground": "text",
                        "background": ["page", "surface"],
                        "kind": "normal-text",
                    }],
                }
            }
        })
        item = report["results"][0]
        self.assertEqual(item["displayed_background"], "#808080")
        self.assertEqual(item["status"], "FAIL")

    def test_alias_cycle_is_rejected(self) -> None:
        with self.assertRaisesRegex(contrast_matrix.ContrastInputError, "alias cycle"):
            contrast_matrix.evaluate_model({
                "themes": {
                    "bad": {
                        "tokens": {"a": "$b", "b": "$a", "page": "#fff"},
                        "pairs": [{"name": "bad", "foreground": "a", "background": ["page"]}],
                    }
                }
            })


class InventoryTests(unittest.TestCase):
    def test_candidates_and_sanctioned_sources_are_reported(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "tokens.css").write_text(":root { --brand: #123456; }\n", encoding="utf-8")
            (root / "Card.tsx").write_text(
                'export const Card = () => <div className="rounded-[7px]" style={{ color: "#fff" }} />;\n',
                encoding="utf-8",
            )
            report = design_value_inventory.inventory([root], sanctioned_patterns=["tokens.css"])
            categories = {item["category"] for item in report["candidates"]}
            self.assertIn("raw-color", categories)
            self.assertIn("tailwind-arbitrary", categories)
            self.assertIn("inline-style", categories)
            token_match = next(item for item in report["candidates"] if item["path"].endswith("tokens.css"))
            self.assertTrue(token_match["sanctioned_source"])


if __name__ == "__main__":
    unittest.main()
