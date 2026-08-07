from __future__ import annotations

import tempfile
import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from migrate_work_artifacts import MigrationError, apply_moves, discover


class MigrationTests(unittest.TestCase):
    def make_repo(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory()
        return temporary, Path(temporary.name)

    def test_discovery_is_read_only_and_classifies_signatures(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        artifact = root / "audits" / "billing"
        artifact.mkdir(parents=True)
        (artifact / "INVARIANTS.md").write_text("billing", encoding="utf-8")
        moves, errors = discover(root)
        self.assertEqual([], errors)
        self.assertEqual("stripe-audit", moves[0].skill)
        self.assertTrue(artifact.exists())

    def test_apply_moves_and_writes_index(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        artifact = root / "plans" / "retry-policy"
        artifact.mkdir(parents=True)
        (artifact / "PLAN.md").write_text("plan", encoding="utf-8")
        moves, errors = discover(root)
        self.assertEqual([], errors)
        journal = root / "migration-journal.json"
        apply_moves(root, moves, journal_path=journal)
        destination = root / "agent-work" / "retry-policy" / "planpro"
        self.assertEqual("plan", (destination / "PLAN.md").read_text(encoding="utf-8"))
        self.assertTrue((destination.parent / "WORK.md").is_file())
        self.assertFalse((root / "plans").exists())
        self.assertEqual("completed", __import__("json").loads(journal.read_text(encoding="utf-8"))["state"])

    def test_release_slug_uses_canonical_release_v_prefix(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        artifact = root / "releases" / "v2.4.0"
        artifact.mkdir(parents=True)
        (artifact / "RELEASE.md").write_text("release", encoding="utf-8")
        moves, errors = discover(root)
        self.assertEqual([], errors)
        self.assertEqual("release-v2-4-0", moves[0].slug)

    def test_changed_source_stops_all_moves_before_mutation(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        first = root / "plans" / "first"
        second = root / "plans" / "second"
        first.mkdir(parents=True)
        second.mkdir(parents=True)
        (first / "PLAN.md").write_text("first", encoding="utf-8")
        (second / "PLAN.md").write_text("second", encoding="utf-8")
        moves, errors = discover(root)
        self.assertEqual([], errors)
        (second / "PLAN.md").write_text("changed", encoding="utf-8")
        with self.assertRaises(MigrationError):
            apply_moves(root, moves, journal_path=root / "journal.json")
        self.assertTrue(first.is_dir())
        self.assertTrue(second.is_dir())
        self.assertFalse((root / "agent-work" / "first").exists())

    def test_existing_work_index_is_updated_without_replacement(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        artifact = root / "plans" / "retry-policy"
        artifact.mkdir(parents=True)
        (artifact / "PLAN.md").write_text("plan", encoding="utf-8")
        slug_root = root / "agent-work" / "retry-policy"
        slug_root.mkdir(parents=True)
        original = "# Work: retry-policy\n\n## Outcome\n\nKeep me.\n"
        (slug_root / "WORK.md").write_text(original, encoding="utf-8")
        moves, errors = discover(root)
        self.assertEqual([], errors)
        apply_moves(root, moves, journal_path=root / "journal.json")
        updated = (slug_root / "WORK.md").read_text(encoding="utf-8")
        self.assertIn(original.strip(), updated)
        self.assertIn("## Migration history", updated)
        self.assertIn("planpro", updated)

    def test_collision_stops_discovery(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        (root / "goals" / "ship").mkdir(parents=True)
        (root / "agent-work" / "ship" / "goalpro").mkdir(parents=True)
        moves, errors = discover(root)
        self.assertEqual([], moves)
        self.assertTrue(any("collision" in error for error in errors))

    def test_unclassified_root_file_is_an_error(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        (root / "plans").mkdir()
        (root / "plans" / "loose.md").write_text("unsafe", encoding="utf-8")
        _, errors = discover(root)
        self.assertTrue(any("unclassified file" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
