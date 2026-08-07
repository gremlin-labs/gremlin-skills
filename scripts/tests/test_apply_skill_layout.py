from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

from apply_skill_layout import LayoutMigrationError, apply_layout, rollback_layout, seal_layout  # noqa: E402
from prepare_skill_layout import build_manifest, validate_manifest, write_manifest  # noqa: E402
from skill_registry import load_registry  # noqa: E402


class ApplySkillLayoutTests(unittest.TestCase):
    def make_repo(self) -> tuple[tempfile.TemporaryDirectory[str], Path, Path, Path, dict]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name) / "repo"
        fixture = Path(__file__).resolve().parent / "fixtures" / "valid-repo"
        shutil.copytree(fixture, root)
        sample = root / "skills" / "sample-skill"
        beta = root / "skills" / "beta"
        shutil.copytree(sample, beta)
        beta_skill = beta / "SKILL.md"
        beta_skill.write_text(
            beta_skill.read_text(encoding="utf-8")
            .replace("name: sample-skill", "name: beta")
            .replace("agent-work/{slug}/sample-skill/", "agent-work/{slug}/beta/"),
            encoding="utf-8",
        )
        sample_skill = sample / "SKILL.md"
        sample_skill.write_text(
            sample_skill.read_text(encoding="utf-8") + "\nSee [Beta](../beta/SKILL.md).\n",
            encoding="utf-8",
        )
        registry_path = root / "skills" / "registry.json"
        registry_data = json.loads(registry_path.read_text(encoding="utf-8"))
        registry_data["category_model"]["values"].append("experience")
        beta_record = json.loads(json.dumps(registry_data["skills"][0]))
        beta_record["name"] = "beta"
        beta_record["category"] = "experience"
        beta_record["path"] = "skills/beta"
        beta_record["output_root"] = "agent-work/{slug}/beta/"
        beta_record["public_docs"]["path"] = "docs/skills/beta.md"
        registry_data["skills"].insert(0, beta_record)
        registry_path.write_text(json.dumps(registry_data, indent=2) + "\n", encoding="utf-8")
        manifest = build_manifest(root, load_registry(root))
        manifest_path = root / "migrations" / "skill-layout-v2.json"
        write_manifest(manifest_path, manifest)
        journal_path = root / "migrations" / "skill-layout-v2-journal.json"
        return temporary, root, manifest_path, journal_path, manifest

    def test_apply_and_rollback_preserve_exact_pre_move_bytes(self) -> None:
        temporary, root, manifest_path, journal_path, manifest = self.make_repo()
        self.addCleanup(temporary.cleanup)
        registry_path = root / "skills" / "registry.json"
        registry_before = registry_path.read_bytes()
        manifest_before = manifest_path.read_bytes()
        source_before = {
            path.relative_to(root): path.read_bytes()
            for path in sorted((root / "skills").rglob("*"))
            if path.is_file()
        }
        confirmation = f"sha256:{manifest['proposal_sha256']}"

        journal = apply_layout(root, manifest_path, journal_path, confirmation)
        self.assertEqual("applied", journal["state"])
        self.assertFalse((root / "skills" / "sample-skill").exists())
        moved = root / "skills" / "engineering" / "sample-skill" / "SKILL.md"
        self.assertIn("../../experience/beta/SKILL.md", moved.read_text(encoding="utf-8"))
        moved_registry = load_registry(root)
        moved_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        state, errors = validate_manifest(root, moved_registry, moved_manifest)
        self.assertEqual("post-move", state)
        self.assertEqual([], errors)

        journal = rollback_layout(root, manifest_path, journal_path, confirmation)
        self.assertEqual("rolled-back", journal["state"])
        self.assertEqual(registry_before, registry_path.read_bytes())
        self.assertEqual(manifest_before, manifest_path.read_bytes())
        source_after = {
            path.relative_to(root): path.read_bytes()
            for path in sorted((root / "skills").rglob("*"))
            if path.is_file()
        }
        self.assertEqual(source_before, source_after)

    def test_exact_confirmation_is_required_before_any_move(self) -> None:
        temporary, root, manifest_path, journal_path, manifest = self.make_repo()
        self.addCleanup(temporary.cleanup)
        with self.assertRaisesRegex(LayoutMigrationError, "exact owner confirmation required"):
            apply_layout(root, manifest_path, journal_path, "sha256:" + "0" * 64)
        self.assertTrue((root / "skills" / "sample-skill").is_dir())
        self.assertFalse(journal_path.exists())

    def test_injected_failure_recovers_the_validated_pre_move_state(self) -> None:
        temporary, root, manifest_path, journal_path, manifest = self.make_repo()
        self.addCleanup(temporary.cleanup)
        registry_before = (root / "skills" / "registry.json").read_bytes()
        manifest_before = manifest_path.read_bytes()
        confirmation = f"sha256:{manifest['proposal_sha256']}"
        with self.assertRaisesRegex(LayoutMigrationError, "injected layout migration failure"):
            apply_layout(root, manifest_path, journal_path, confirmation, fail_after=1)
        self.assertEqual(registry_before, (root / "skills" / "registry.json").read_bytes())
        self.assertEqual(manifest_before, manifest_path.read_bytes())
        self.assertTrue((root / "skills" / "sample-skill").is_dir())
        self.assertEqual("rolled-back", json.loads(journal_path.read_text(encoding="utf-8"))["state"])

    def test_post_apply_drift_refuses_rollback(self) -> None:
        temporary, root, manifest_path, journal_path, manifest = self.make_repo()
        self.addCleanup(temporary.cleanup)
        confirmation = f"sha256:{manifest['proposal_sha256']}"
        apply_layout(root, manifest_path, journal_path, confirmation)
        moved = root / "skills" / "engineering" / "sample-skill" / "SKILL.md"
        moved.write_text(moved.read_text(encoding="utf-8") + "\nDrift.\n", encoding="utf-8")
        with self.assertRaisesRegex(LayoutMigrationError, "post-move state"):
            rollback_layout(root, manifest_path, journal_path, confirmation)
        self.assertTrue(moved.is_file())

    def test_seal_closes_rollback_window_and_allows_later_skill_edits(self) -> None:
        temporary, root, manifest_path, journal_path, manifest = self.make_repo()
        self.addCleanup(temporary.cleanup)
        confirmation = f"sha256:{manifest['proposal_sha256']}"
        apply_layout(root, manifest_path, journal_path, confirmation)
        journal = seal_layout(root, manifest_path, journal_path, confirmation)
        self.assertEqual("sealed", journal["state"])
        moved = root / "skills" / "engineering" / "sample-skill" / "SKILL.md"
        moved.write_text(moved.read_text(encoding="utf-8") + "\nMaintained.\n", encoding="utf-8")
        moved_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        state, errors = validate_manifest(root, load_registry(root), moved_manifest)
        self.assertEqual("post-move", state)
        self.assertEqual([], errors)
        with self.assertRaisesRegex(LayoutMigrationError, "sealed"):
            rollback_layout(root, manifest_path, journal_path, confirmation)


if __name__ == "__main__":
    unittest.main()
