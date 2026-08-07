from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

from validate_public_release import validate_public_release  # noqa: E402


class PublicReleaseValidatorTests(unittest.TestCase):
    def make_repo(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        (root / ".gitignore").write_text(
            "/agent-work/\n/dist/\n/references/\n/research/\n/node_modules/\n__pycache__/\n*.bundle\n.DS_Store\n/.trufflehog-exclude-paths.txt\n",
            encoding="utf-8",
        )
        (root / "README.md").write_text("# Safe\n\nUse `$HOME/project`.\n", encoding="utf-8")
        return temporary, root

    def test_safe_public_tree_passes_and_excluded_work_is_not_scanned(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        private = root / "agent-work" / "private"
        private.mkdir(parents=True)
        ignored_path = "/" + "Users" + "/private/work"
        private.joinpath("NOTES.md").write_text(f"{ignored_path}\n", encoding="utf-8")
        count, errors = validate_public_release(root)
        self.assertEqual(2, count)
        self.assertEqual([], errors)

    def test_local_paths_and_token_shapes_fail_without_echoing_values(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        token = "github" + "_pat_" + "A" * 30
        local_path = "/" + "Users" + "/person/project"
        path = root / "unsafe.md"
        path.write_text(f"{local_path}\n{token}\n", encoding="utf-8")
        _, errors = validate_public_release(root)
        self.assertTrue(any("macOS user path" in error for error in errors), errors)
        self.assertTrue(any("possible GitHub token" in error for error in errors), errors)
        self.assertNotIn(token, "\n".join(errors))

    def test_trufflehog_exclusion_rules_remain_private(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        rules = root / ".trufflehog-exclude-paths.txt"
        rules.write_text("private scanner configuration\n", encoding="utf-8")
        count, errors = validate_public_release(root)
        self.assertEqual(2, count)
        self.assertEqual([], errors)

    def test_missing_ignore_and_license_are_explicit(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        ignore = root / ".gitignore"
        ignore.write_text(ignore.read_text(encoding="utf-8").replace("/research/\n", ""), encoding="utf-8")
        _, errors = validate_public_release(root, require_license=True)
        self.assertTrue(any("/research/" in error for error in errors), errors)
        self.assertTrue(any("owner-approved open-source license" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
