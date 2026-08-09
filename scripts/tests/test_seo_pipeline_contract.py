from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class SeoPipelineContractTests(unittest.TestCase):
    def setUp(self) -> None:
        registry = json.loads((ROOT / "skills" / "registry.json").read_text(encoding="utf-8"))
        self.records = {record["name"]: record for record in registry["skills"]}

    def test_autonomous_page_routes_are_model_visible(self) -> None:
        for name in ("seo-foundation", "seo-strategy", "seo-content", "landing-page", "seo-monitor"):
            with self.subTest(skill=name):
                self.assertEqual("model-visible", self.records[name]["invocation"]["mode"])

    def test_external_provider_stages_remain_explicit_only(self) -> None:
        for name in ("seo-setup", "seo-indexing"):
            with self.subTest(skill=name):
                self.assertEqual("user-only", self.records[name]["invocation"]["mode"])

    def test_page_specialists_share_the_page_quality_contract(self) -> None:
        for name in ("seo-content", "landing-page"):
            with self.subTest(skill=name):
                self.assertIn("seo-page-quality", self.records[name]["contracts"])

    def test_strategy_cannot_restore_page_briefs_or_goalpro_page_fallback(self) -> None:
        strategy = (ROOT / "skills" / "growth" / "seo-strategy" / "SKILL.md").read_text(encoding="utf-8")
        artifact_data = json.loads((ROOT / "evals" / "artifact-contracts.json").read_text(encoding="utf-8"))
        contract = next(item for item in artifact_data["contracts"] if item["skill"] == "seo-strategy")
        paths = {item["path"] for item in contract["files"]}
        self.assertNotIn("LANDING-PAGE-BRIEFS.md", paths)
        self.assertNotIn("EDITORIAL-BRIEFS.md", paths)
        self.assertIn("PAGE-OPPORTUNITIES.md", paths)
        self.assertIn("never route page work through Goalpro as a fallback", strategy)


if __name__ == "__main__":
    unittest.main()
