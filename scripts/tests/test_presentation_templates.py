from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTRACTS = ROOT / "evals" / "artifact-contracts.json"
REGISTRY = ROOT / "skills" / "registry.json"


def skill_path(name: str) -> Path:
    records = json.loads(REGISTRY.read_text(encoding="utf-8"))["skills"]
    record = next(item for item in records if item["name"] == name)
    return ROOT / record["path"]


class PresentationTemplateContractTests(unittest.TestCase):
    def test_templates_cover_every_required_markdown_heading(self) -> None:
        contracts = json.loads(CONTRACTS.read_text(encoding="utf-8"))["contracts"]
        contract = next(
            item for item in contracts if item["skill"] == "turbulencejs-presentation"
        )
        templates = skill_path("turbulencejs-presentation") / "templates"

        for artifact in contract["files"]:
            if not artifact["required"] or not artifact["path"].endswith(".md"):
                continue

            template = templates / artifact["path"]
            self.assertTrue(template.is_file(), f"missing template: {template}")
            headings = {
                match.group(1).strip()
                for line in template.read_text(encoding="utf-8").splitlines()
                if (match := re.match(r"^#{1,6}\s+(.+?)\s*$", line))
            }
            for required_heading in artifact["headings"]:
                self.assertIn(
                    required_heading,
                    headings,
                    f"{template.name} is missing heading {required_heading!r}",
                )


if __name__ == "__main__":
    unittest.main()
