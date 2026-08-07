from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

from run_skill_tests import run_skill_tests  # noqa: E402


class SkillTestRunnerTests(unittest.TestCase):
    def make_repo(self, source: str = "raise SystemExit(0)\n") -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name) / "repo"
        fixture = Path(__file__).resolve().parent / "fixtures" / "valid-repo"
        shutil.copytree(fixture, root)
        script = root / "skills" / "sample-skill" / "scripts" / "test_runner.py"
        script.parent.mkdir()
        script.write_text(source, encoding="utf-8")
        registry_path = root / "skills" / "registry.json"
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        registry["skills"][0]["tests"] = ["python3 skills/sample-skill/scripts/test_runner.py"]
        registry_path.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
        return temporary, root

    def test_declared_suite_passes_without_shell(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        receipt, errors = run_skill_tests(root)
        self.assertEqual([], errors)
        self.assertEqual(1, receipt["summary"]["declared_suites"])
        self.assertEqual("PASSED", receipt["results"][0]["status"])

    def test_failure_is_recorded_without_output_in_receipt(self) -> None:
        temporary, root = self.make_repo("print('fixture output')\nraise SystemExit(4)\n")
        self.addCleanup(temporary.cleanup)
        receipt, errors = run_skill_tests(root)
        self.assertTrue(errors)
        self.assertEqual("FAILED", receipt["results"][0]["status"])
        self.assertNotIn("fixture output", json.dumps(receipt))

    def test_unavailable_runtime_is_explicit(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        with mock.patch("run_skill_tests.shutil.which", return_value=None):
            receipt, errors = run_skill_tests(root)
        self.assertTrue(errors)
        self.assertEqual("UNAVAILABLE", receipt["results"][0]["status"])

    def test_shell_command_is_rejected(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        registry_path = root / "skills" / "registry.json"
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        registry["skills"][0]["tests"] = ["bash skills/sample-skill/scripts/test_runner.py"]
        registry_path.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
        receipt, errors = run_skill_tests(root)
        self.assertTrue(any("approved no-shell executable" in error for error in errors), errors)
        self.assertEqual("FAILED", receipt["results"][0]["status"])


if __name__ == "__main__":
    unittest.main()
