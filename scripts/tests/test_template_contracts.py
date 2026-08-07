from __future__ import annotations

import json
import re
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTRACTS = {
    contract["skill"]: contract
    for contract in json.loads((ROOT / "evals" / "artifact-contracts.json").read_text(encoding="utf-8"))["contracts"]
}
WORK_HEADINGS = {
    "Outcome",
    "Ownership",
    "Status",
    "Stages",
    "Current handoff",
    "Decisions and material deltas",
    "Final evidence",
}


def headings(path: Path) -> set[str]:
    return {
        match.group(1).strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if (match := re.match(r"^#{1,6}\s+(.+?)\s*$", line))
    }


class TemplateContractTests(unittest.TestCase):
    def test_every_template_is_consumed_and_matches_an_artifact_contract(self) -> None:
        template_directories = sorted(
            path
            for path in (ROOT / "skills").rglob("templates")
            if path.is_dir() and (path.parent / "SKILL.md").is_file()
        )
        self.assertTrue(template_directories)
        for directory in template_directories:
            skill = directory.parent.name
            instruction_text = "\n".join(
                path.read_text(encoding="utf-8") for path in directory.parent.glob("*.md")
            )
            self.assertTrue(
                "templates/" in instruction_text
                or "bundled templates" in instruction_text
                or "from the templates" in instruction_text,
                f"{skill} does not tell agents to consume bundled templates",
            )
            contracts = {item["path"]: item for item in CONTRACTS[skill]["files"]}
            for template in sorted(directory.rglob("*")):
                if not template.is_file():
                    continue
                self.assertFalse(template.is_symlink(), f"template must not be a symlink: {template}")
                self.assertGreater(template.stat().st_size, 0, f"empty template: {template}")
                relative = template.relative_to(directory).as_posix()
                if relative == "WORK.md":
                    self.assertTrue(WORK_HEADINGS.issubset(headings(template)), template)
                    continue
                self.assertIn(relative, contracts, f"uncontracted template: {skill}/{relative}")
                self.assertTrue(set(contracts[relative]["headings"]).issubset(headings(template)), template)

    def test_templates_can_be_instantiated_without_modifying_sources(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            for directory in sorted(
                path
                for path in (ROOT / "skills").rglob("templates")
                if path.is_dir() and (path.parent / "SKILL.md").is_file()
            ):
                for template in sorted(directory.rglob("*")):
                    if not template.is_file():
                        continue
                    target = output / directory.parent.name / template.relative_to(directory)
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text(
                        template.read_text(encoding="utf-8").replace("{slug}", "example-skill-work").replace("{title}", "Example work"),
                        encoding="utf-8",
                    )
                    self.assertTrue(target.is_file())
                    self.assertGreater(target.stat().st_size, 0)


if __name__ == "__main__":
    unittest.main()
