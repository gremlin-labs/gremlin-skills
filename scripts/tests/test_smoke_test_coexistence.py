from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

from smoke_test_coexistence import CoexistenceError, smoke_test  # noqa: E402


class CoexistenceSmokeTests(unittest.TestCase):
    def make_repo(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name) / "repo"
        fixture = Path(__file__).resolve().parent / "fixtures" / "valid-repo"
        shutil.copytree(fixture, root)
        return temporary, root

    def test_both_install_orders_preserve_foreign_content(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        receipt = smoke_test(root, ["reference-skill"])
        self.assertEqual("offline-synthetic-foreign-library", receipt["proof_mode"])
        self.assertEqual(2, len(receipt["orders"]))
        self.assertTrue(receipt["claims"]["foreign_content_unchanged"])
        self.assertFalse(receipt["claims"]["real_upstream_installer_exercised"])

    def test_collision_is_rejected_before_install(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        with self.assertRaisesRegex(CoexistenceError, "identity collision"):
            smoke_test(root, ["sample-skill"])

    def test_foreign_identities_must_be_sorted_and_unique(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        with self.assertRaisesRegex(CoexistenceError, "unique, and sorted"):
            smoke_test(root, ["zeta-skill", "alpha-skill", "alpha-skill"])


if __name__ == "__main__":
    unittest.main()
