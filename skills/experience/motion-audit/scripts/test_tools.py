#!/usr/bin/env python3
"""Unit tests for Motion Audit deterministic helpers."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from motion_inventory import inventory


class MotionInventoryTests(unittest.TestCase):
    def test_finds_motion_and_accessibility_candidates(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "app.css").write_text(
                ".menu { transition: transform 180ms ease; }\n"
                "@media (prefers-reduced-motion: reduce) { .menu { transition: none; } }\n",
                encoding="utf-8",
            )
            candidates = inventory(root)
            kinds = {kind for candidate in candidates for kind in candidate["kinds"]}
            self.assertIn("css-transition", kinds)
            self.assertIn("reduced-motion", kinds)

    def test_skips_dependencies(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            dependency = root / "node_modules" / "pkg"
            dependency.mkdir(parents=True)
            (dependency / "index.js").write_text("requestAnimationFrame(loop);", encoding="utf-8")
            self.assertEqual(inventory(root), [])

    def test_finds_turbulencejs_imports(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "motion.ts").write_text(
                "import cinematic from 'turbulencejs/cinematic';\n",
                encoding="utf-8",
            )
            candidates = inventory(root)
            self.assertEqual(candidates[0]["kinds"], ["motion-library"])


if __name__ == "__main__":
    unittest.main()
