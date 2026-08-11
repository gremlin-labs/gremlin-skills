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

    def test_change_control_consumers_are_exact(self) -> None:
        expected = {"goalpro", "landing-page", "seo-content", "seo-monitor", "seo-strategy"}
        actual = {
            name
            for name, record in self.records.items()
            if "seo-change-control" in record["contracts"]
        }
        self.assertEqual(expected, actual)

    def test_change_control_is_materialized_with_each_consumer(self) -> None:
        for name in ("goalpro", "landing-page", "seo-content", "seo-monitor", "seo-strategy"):
            with self.subTest(skill=name):
                skill_root = next(ROOT.glob(f"skills/*/{name}"))
                self.assertTrue((skill_root / "contracts" / "seo-change-control.md").is_file())
                validator = skill_root / "scripts" / "validate_seo_change_control.py"
                self.assertTrue(validator.is_file())
                self.assertIn("source-sha256:", validator.read_text(encoding="utf-8"))

    def test_strategy_cannot_restore_page_briefs_or_goalpro_page_fallback(self) -> None:
        strategy = (ROOT / "skills" / "growth" / "seo-strategy" / "SKILL.md").read_text(encoding="utf-8")
        artifact_data = json.loads((ROOT / "evals" / "artifact-contracts.json").read_text(encoding="utf-8"))
        contract = next(item for item in artifact_data["contracts"] if item["skill"] == "seo-strategy")
        paths = {item["path"] for item in contract["files"]}
        self.assertNotIn("LANDING-PAGE-BRIEFS.md", paths)
        self.assertNotIn("EDITORIAL-BRIEFS.md", paths)
        self.assertIn("PAGE-OPPORTUNITIES.md", paths)
        self.assertIn("never route page work through Goalpro as a fallback", strategy)
        self.assertIn("SEO-TECHNICAL-SCOPE.json", paths)
        self.assertIn("`user_facing_changes`", strategy)
        self.assertIn("`FORBIDDEN`", strategy)

    def test_goalpro_rejects_unlisted_editorial_changes(self) -> None:
        goalpro = (ROOT / "skills" / "engineering" / "goalpro" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("SEO-TECHNICAL-SCOPE.json", goalpro)
        self.assertIn("unlisted user-facing", goalpro)
        self.assertIn("CONFORMANCE", goalpro)


if __name__ == "__main__":
    unittest.main()
