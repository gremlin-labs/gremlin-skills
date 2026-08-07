#!/usr/bin/env python3
"""Unit tests for the bundled Theme Library catalog."""

from __future__ import annotations

import json
import unittest

from build_palette_master import CATALOG_PATH, MASTER_PATH, build, validate_catalog


class PaletteMasterTests(unittest.TestCase):
    def test_catalog_is_complete_portable_and_in_sync(self) -> None:
        raw = CATALOG_PATH.read_text(encoding="utf-8")
        catalog = json.loads(raw)
        self.assertEqual(validate_catalog(catalog, raw), [])
        self.assertEqual(MASTER_PATH.read_text(encoding="utf-8"), build(catalog))

    def test_catalog_supports_interpretive_selection(self) -> None:
        catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
        self.assertTrue(any(family["swatches"] for family in catalog["families"]))
        self.assertTrue(any(palette.get("roles") for palette in catalog["productPalettes"]))


if __name__ == "__main__":
    unittest.main()
