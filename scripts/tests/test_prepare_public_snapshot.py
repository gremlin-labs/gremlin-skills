from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

from prepare_public_snapshot import build_public_snapshot  # noqa: E402
from validate_public_release import PublicReleaseError  # noqa: E402


class PublicSnapshotTests(unittest.TestCase):
    def make_repo(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        (root / ".gitignore").write_text(
            "/agent-work/\n/dist/\n/references/\n/research/\n/node_modules/\n__pycache__/\n*.bundle\n.DS_Store\n/.trufflehog-exclude-paths.txt\n",
            encoding="utf-8",
        )
        (root / "README.md").write_text("# Public\n", encoding="utf-8")
        private = root / "agent-work"
        private.mkdir()
        private.joinpath("PRIVATE.md").write_text("private\n", encoding="utf-8")
        (root / ".trufflehog-exclude-paths.txt").write_text("private scanner configuration\n", encoding="utf-8")
        return temporary, root

    def test_snapshot_stages_only_public_files_and_is_deterministic(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        first = build_public_snapshot(root)
        second = build_public_snapshot(root)
        self.assertEqual("PASSED", first["status"])
        self.assertEqual(2, first["files"])
        self.assertEqual(first["tree_oid"], second["tree_oid"])
        self.assertEqual([".gitignore", "README.md"], first["paths"])
        self.assertEqual([".gitignore", "README.md"], first["top_level"])
        self.assertIn("agent-work", first["excluded_roots"])

    def test_strict_snapshot_requires_owner_selected_license(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        with self.assertRaisesRegex(PublicReleaseError, "owner-approved open-source license"):
            build_public_snapshot(root, require_license=True)


if __name__ == "__main__":
    unittest.main()
