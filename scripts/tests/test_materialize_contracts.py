from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1]
ROOT = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))

from materialize_contracts import (  # noqa: E402
    GENERATED_PREFIX,
    GENERATED_RESOURCE_PREFIX,
    check_materialized,
    expected_snapshots,
    write_materialized,
)
from skill_registry import load_registry  # noqa: E402


class ContractMaterializationTests(unittest.TestCase):
    def make_repo(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        fixture = Path(__file__).resolve().parent / "fixtures" / "valid-repo"
        shutil.copytree(fixture, root, dirs_exist_ok=True)
        shutil.copytree(ROOT / "contracts", root / "contracts")
        (root / "scripts").mkdir(exist_ok=True)
        shutil.copy2(
            ROOT / "scripts" / "validate_seo_change_control.py",
            root / "scripts" / "validate_seo_change_control.py",
        )
        return temporary, root

    def assert_has_error(self, errors: list[str], phrase: str) -> None:
        self.assertTrue(any(phrase in error for error in errors), errors)

    def test_current_repository_snapshots_are_exact(self) -> None:
        registry = load_registry(ROOT)
        self.assertEqual(127, len(expected_snapshots(ROOT, registry)))
        self.assertEqual([], check_materialized(ROOT, registry))
        for skill in ("goalpro", "landing-page", "seo-content", "seo-monitor", "seo-strategy"):
            validator = next(
                ROOT.glob(f"skills/*/{skill}/scripts/validate_seo_change_control.py")
            )
            self.assertIn(GENERATED_RESOURCE_PREFIX, validator.read_text(encoding="utf-8"))

    def test_write_then_check_materializes_digest_stamped_snapshot(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        registry = load_registry(root)
        written, removed = write_materialized(root, registry)
        self.assertEqual((1, 0), (written, removed))
        self.assertEqual([], check_materialized(root, registry))
        snapshot = root / "skills" / "sample-skill" / "contracts" / "work-artifacts.md"
        text = snapshot.read_text(encoding="utf-8")
        self.assertTrue(text.startswith(GENERATED_PREFIX))
        self.assertIn("source-sha256:", text)

    def test_tampered_snapshot_is_stale(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        registry = load_registry(root)
        write_materialized(root, registry)
        snapshot = root / "skills" / "sample-skill" / "contracts" / "work-artifacts.md"
        snapshot.write_text(snapshot.read_text() + "tampered\n", encoding="utf-8")
        self.assert_has_error(check_materialized(root, registry), "stale generated contract snapshot")

    def test_source_change_invalidates_snapshot(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        registry = load_registry(root)
        write_materialized(root, registry)
        source = root / "contracts" / "work-artifacts.md"
        source.write_text(source.read_text() + "\nNew rule.\n", encoding="utf-8")
        self.assert_has_error(check_materialized(root, registry), "stale generated contract snapshot")

    def test_undeclared_generated_snapshot_is_rejected_and_removed(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        registry = load_registry(root)
        write_materialized(root, registry)
        extra = root / "skills" / "sample-skill" / "contracts" / "extra.md"
        extra.write_text(GENERATED_PREFIX + "contract: extra\n-->\n", encoding="utf-8")
        self.assert_has_error(check_materialized(root, registry), "undeclared generated contract snapshot")
        self.assertEqual((0, 1), write_materialized(root, registry))
        self.assertFalse(extra.exists())


if __name__ == "__main__":
    unittest.main()
