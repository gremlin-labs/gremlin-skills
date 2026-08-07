from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

from skill_registry import load_registry  # noqa: E402
from validate_registry import validate_registry  # noqa: E402


class RegistrySourceValidatorTests(unittest.TestCase):
    def make_repo(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        fixture = Path(__file__).resolve().parent / "fixtures" / "valid-repo"
        shutil.copytree(fixture, root, dirs_exist_ok=True)
        evals = root / "evals"
        evals.mkdir()
        contract = {
            "version": 1,
            "contracts": [{
                "skill": "sample-skill",
                "output_root": "agent-work/{slug}/sample-skill/",
                "files": [{"path": "MAIN.md", "required": True, "headings": ["Goal"]}],
            }],
        }
        (evals / "artifact-contracts.json").write_text(json.dumps(contract, indent=2) + "\n", encoding="utf-8")
        return temporary, root

    def assert_has_error(self, errors: list[str], phrase: str) -> None:
        self.assertTrue(any(phrase in error for error in errors), errors)

    def test_valid_registry_matches_source(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        self.assertEqual([], validate_registry(root, load_registry(root)))

    def test_unregistered_skill_source_fails(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        extra = root / "skills" / "extra"
        extra.mkdir()
        (extra / "SKILL.md").write_text("# Extra\n", encoding="utf-8")
        self.assert_has_error(validate_registry(root, load_registry(root)), "unregistered skill source")

    def test_output_contract_drift_fails(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        path = root / "evals" / "artifact-contracts.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["contracts"][0]["output_root"] = "other/"
        path.write_text(json.dumps(data), encoding="utf-8")
        self.assert_has_error(validate_registry(root, load_registry(root)), "does not match artifact contract")

    def test_undeclared_skill_test_fails(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        scripts = root / "skills" / "sample-skill" / "scripts"
        scripts.mkdir()
        (scripts / "test_tools.py").write_text("pass\n", encoding="utf-8")
        self.assert_has_error(validate_registry(root, load_registry(root)), "skill-local test is not declared")

    def test_nested_undeclared_skill_test_fails(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        tests = root / "skills" / "sample-skill" / "scripts" / "tests"
        tests.mkdir(parents=True)
        (tests / "test_nested.py").write_text("pass\n", encoding="utf-8")
        self.assert_has_error(validate_registry(root, load_registry(root)), "skill-local test is not declared")

    def test_linked_dependency_must_be_declared(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        registry_path = root / "skills" / "registry.json"
        data = json.loads(registry_path.read_text(encoding="utf-8"))
        other = json.loads(json.dumps(data["skills"][0]))
        other["name"] = "other-skill"
        other["path"] = "skills/other-skill"
        other["public_docs"]["path"] = "docs/skills/other-skill.md"
        other["output_root"] = "agent-work/{slug}/other-skill/"
        data["skills"].append(other)
        data["skills"].sort(key=lambda record: record["name"])
        registry_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        other_dir = root / "skills" / "other-skill"
        shutil.copytree(root / "skills" / "sample-skill", other_dir)
        other_skill = other_dir / "SKILL.md"
        other_skill.write_text(other_skill.read_text().replace("sample-skill", "other-skill"), encoding="utf-8")
        sample = root / "skills" / "sample-skill" / "SKILL.md"
        sample.write_text(sample.read_text() + "\nSee [Other](../other-skill/SKILL.md).\n", encoding="utf-8")
        contracts = json.loads((root / "evals" / "artifact-contracts.json").read_text())
        contracts["contracts"].append({
            "skill": "other-skill",
            "output_root": "agent-work/{slug}/other-skill/",
            "files": [{"path": "MAIN.md", "required": True, "headings": ["Goal"]}],
        })
        (root / "evals" / "artifact-contracts.json").write_text(json.dumps(contracts), encoding="utf-8")
        self.assert_has_error(validate_registry(root, load_registry(root)), "is not declared as a dependency")

    def test_linked_local_contract_must_be_declared(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        skill = root / "skills" / "sample-skill"
        (skill / "contracts" / "execution-quality.md").write_text("# Quality\n", encoding="utf-8")
        path = skill / "SKILL.md"
        path.write_text(
            path.read_text() + "\nSee [quality](contracts/execution-quality.md).\n",
            encoding="utf-8",
        )
        self.assert_has_error(validate_registry(root, load_registry(root)), "local contract 'quality' is not declared")


if __name__ == "__main__":
    unittest.main()
