from __future__ import annotations

import shutil
import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

from validate_skills import validate_repo  # noqa: E402


SKILL = """---
name: sample-skill
description: Performs a useful sample workflow. Use when testing the repository validator.
---

# Sample skill

```dot
digraph sample { start -> done; }
```

See [REFERENCE.md](REFERENCE.md).
See [work-artifact contract](contracts/work-artifacts.md).

Write to `agent-work/{slug}/sample-skill/`.

## Optional shared Theme Library

Discover an independently installed Theme Library through the host registry or sibling skill directory.
"""

class SkillValidatorTests(unittest.TestCase):
    def make_repo(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        fixture = Path(__file__).resolve().parent / "fixtures" / "valid-repo"
        shutil.copytree(fixture, root, dirs_exist_ok=True)
        return temporary, root

    def assert_has_error(self, errors: list[str], phrase: str) -> None:
        self.assertTrue(any(phrase in error for error in errors), errors)

    def test_valid_repository(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        names, errors = validate_repo(root)
        self.assertEqual(["sample-skill"], names)
        self.assertEqual([], errors)

    def test_mismatched_name(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        path = root / "skills" / "sample-skill" / "SKILL.md"
        path.write_text(SKILL.replace("name: sample-skill", "name: wrong-name"), encoding="utf-8")
        self.assert_has_error(validate_repo(root)[1], "does not match directory")

    def test_missing_use_when(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        path = root / "skills" / "sample-skill" / "SKILL.md"
        path.write_text(SKILL.replace(" Use when testing the repository validator.", ""), encoding="utf-8")
        self.assert_has_error(validate_repo(root)[1], "followed by 'Use when'")

    def test_missing_decision_tree(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        path = root / "skills" / "sample-skill" / "SKILL.md"
        path.write_text(SKILL.replace("```dot", "```text"), encoding="utf-8")
        self.assert_has_error(validate_repo(root)[1], "decision tree")

    def test_missing_work_artifact_contract(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        path = root / "skills" / "sample-skill" / "SKILL.md"
        path.write_text(SKILL.replace("See [work-artifact contract](contracts/work-artifacts.md).\n", ""), encoding="utf-8")
        self.assert_has_error(validate_repo(root)[1], "missing generated local work-artifact contract link")

    def test_missing_theme_library_discovery(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        path = root / "skills" / "sample-skill" / "SKILL.md"
        text = path.read_text(encoding="utf-8")
        text = text.replace("\n## Optional shared Theme Library\n\nDiscover an independently installed Theme Library through the host registry or sibling skill directory.\n", "")
        path.write_text(text, encoding="utf-8")
        self.assert_has_error(validate_repo(root)[1], "Theme Library discovery contract")

    def test_compact_history_uses_reserved_root_exception(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        old = root / "skills" / "sample-skill"
        new = root / "skills" / "compact-history"
        old.rename(new)
        skill = (new / "SKILL.md").read_text(encoding="utf-8")
        skill = skill.replace("sample-skill", "compact-history").replace(
            "agent-work/{slug}/compact-history/", "agent-work/• compact-history/"
        )
        (new / "SKILL.md").write_text(skill, encoding="utf-8")
        metadata = new / "agents" / "openai.yaml"
        metadata.write_text(
            metadata.read_text(encoding="utf-8")
            .replace("Sample Skill", "Compact History")
            .replace("sample-skill", "compact-history"),
            encoding="utf-8",
        )
        registry_path = root / "skills" / "registry.json"
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        record = registry["skills"][0]
        record["name"] = "compact-history"
        record["path"] = "skills/compact-history"
        record["public_docs"]["path"] = "docs/skills/compact-history.md"
        record["output_root"] = "agent-work/• compact-history/"
        registry_path.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
        (root / "README.md").write_text(
            "# Fixture\n\n```text\nskills/\n└── compact-history/ # fixture\n```\n\n### compact-history — fixture\n",
            encoding="utf-8",
        )
        self.assertEqual([], validate_repo(root)[1])

    def test_legacy_generated_root(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        path = root / "skills" / "sample-skill" / "SKILL.md"
        path.write_text(SKILL + "\nWrite to `plans/{slug}/`.\n", encoding="utf-8")
        self.assert_has_error(validate_repo(root)[1], "legacy generated-work root")

    def test_broken_link(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        (root / "skills" / "sample-skill" / "REFERENCE.md").unlink()
        self.assert_has_error(validate_repo(root)[1], "broken relative link")

    def test_xml_placeholder(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        path = root / "skills" / "sample-skill" / "REFERENCE.md"
        path.write_text("# Reference\n\nUse <slug>.\n", encoding="utf-8")
        self.assert_has_error(validate_repo(root)[1], "XML-like placeholder")

    def test_initializer_marker(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        path = root / "skills" / "sample-skill" / "REFERENCE.md"
        path.write_text("# Reference\n\nTODO finish.\n", encoding="utf-8")
        self.assert_has_error(validate_repo(root)[1], "initializer marker")

    def test_readme_omission(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        (root / "README.md").write_text("# Empty index\n", encoding="utf-8")
        errors = validate_repo(root)[1]
        self.assert_has_error(errors, "missing from catalog")

    def test_malformed_ui_metadata(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        agents = root / "skills" / "sample-skill" / "agents"
        agents.mkdir(exist_ok=True)
        (agents / "openai.yaml").write_text(
            'interface:\n  display_name: Sample\n  short_description: "Sample skill"\n  default_prompt: "Use this."\n',
            encoding="utf-8",
        )
        errors = validate_repo(root)[1]
        self.assert_has_error(errors, "display_name")
        self.assert_has_error(errors, "default_prompt must mention")

    def test_global_sync_matching_missing_and_divergent(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        global_root = root / "global"
        global_root.mkdir()
        errors = validate_repo(root, global_root)[1]
        self.assert_has_error(errors, "installed skill is missing")

        shutil.copytree(root / "skills" / "sample-skill", global_root / "sample-skill")
        self.assertEqual([], validate_repo(root, global_root)[1])

        cache = global_root / "sample-skill" / "scripts" / "__pycache__"
        cache.mkdir(parents=True)
        (cache / "runtime.pyc").write_bytes(b"runtime cache")
        self.assertEqual([], validate_repo(root, global_root)[1])

        (global_root / "sample-skill" / "REFERENCE.md").write_text("# Diverged\n", encoding="utf-8")
        self.assert_has_error(validate_repo(root, global_root)[1], "differs from repository copy")


if __name__ == "__main__":
    unittest.main()
