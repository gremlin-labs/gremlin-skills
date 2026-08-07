from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

from sync_installed_skills import (  # noqa: E402
    MANAGED_DIR,
    MANIFEST_NAME,
    SyncError,
    load_manifest,
    rollback_run,
    sync_skills,
)


class InstalledSkillSyncTests(unittest.TestCase):
    def make_repo(self, *, two_skills: bool = False) -> tuple[tempfile.TemporaryDirectory[str], Path, Path]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name) / "repo"
        target = Path(temporary.name) / "installed"
        fixture = Path(__file__).resolve().parent / "fixtures" / "valid-repo"
        shutil.copytree(fixture, root)
        if two_skills:
            registry_path = root / "skills" / "registry.json"
            registry = json.loads(registry_path.read_text(encoding="utf-8"))
            second = json.loads(json.dumps(registry["skills"][0]))
            second["name"] = "second-skill"
            second["path"] = "skills/second-skill"
            second["public_docs"]["path"] = "docs/skills/second-skill.md"
            second["output_root"] = "agent-work/{slug}/second-skill/"
            registry["skills"].append(second)
            registry["skills"].sort(key=lambda record: record["name"])
            registry_path.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
            source = root / "skills" / "sample-skill"
            destination = root / "skills" / "second-skill"
            shutil.copytree(source, destination)
            skill = destination / "SKILL.md"
            skill.write_text(skill.read_text().replace("sample-skill", "second-skill"), encoding="utf-8")
        return temporary, root, target

    def test_dry_run_has_no_side_effects(self) -> None:
        temporary, root, target = self.make_repo()
        self.addCleanup(temporary.cleanup)
        plan = sync_skills(root, target, ["sample-skill"], run_id="dry-run")
        self.assertEqual("dry-run", plan["mode"])
        self.assertEqual("install", plan["operations"][0]["action"])
        self.assertFalse(target.exists())

    def test_foreign_unowned_path_is_refused(self) -> None:
        temporary, root, target = self.make_repo()
        self.addCleanup(temporary.cleanup)
        foreign = target / "sample-skill"
        foreign.mkdir(parents=True)
        (foreign / "SKILL.md").write_text("foreign\n", encoding="utf-8")
        with self.assertRaisesRegex(SyncError, "foreign unowned path"):
            sync_skills(root, target, ["sample-skill"], run_id="foreign")

    def test_apply_records_exact_ownership_and_ignores_cache_noise(self) -> None:
        temporary, root, target = self.make_repo()
        self.addCleanup(temporary.cleanup)
        journal = sync_skills(root, target, ["sample-skill"], apply=True, run_id="install-one")
        self.assertEqual("complete", journal["status"])
        manifest = load_manifest(target)
        self.assertIn("sample-skill", manifest["skills"])
        cache = target / "sample-skill" / "scripts" / "__pycache__"
        cache.mkdir(parents=True)
        (cache / "runtime.pyc").write_bytes(b"runtime")
        plan = sync_skills(root, target, ["sample-skill"], run_id="cache-noise")
        self.assertEqual("noop", plan["operations"][0]["action"])

    def test_locally_modified_owned_skill_is_refused(self) -> None:
        temporary, root, target = self.make_repo()
        self.addCleanup(temporary.cleanup)
        sync_skills(root, target, ["sample-skill"], apply=True, run_id="install-one")
        path = target / "sample-skill" / "REFERENCE.md"
        path.write_text("local change\n", encoding="utf-8")
        with self.assertRaisesRegex(SyncError, "locally modified owned skill"):
            sync_skills(root, target, ["sample-skill"], run_id="refuse-local")

    def test_update_then_rollback_restores_prior_tree_and_manifest(self) -> None:
        temporary, root, target = self.make_repo()
        self.addCleanup(temporary.cleanup)
        sync_skills(root, target, ["sample-skill"], apply=True, run_id="first")
        installed_before = (target / "sample-skill" / "REFERENCE.md").read_bytes()
        manifest_before = load_manifest(target)
        source = root / "skills" / "sample-skill" / "REFERENCE.md"
        source.write_text(source.read_text() + "\nUpdated.\n", encoding="utf-8")
        sync_skills(root, target, ["sample-skill"], apply=True, run_id="second")
        self.assertNotEqual(installed_before, (target / "sample-skill" / "REFERENCE.md").read_bytes())
        journal = rollback_run(target, "second")
        self.assertEqual("rolled-back", journal["status"])
        self.assertEqual(installed_before, (target / "sample-skill" / "REFERENCE.md").read_bytes())
        self.assertEqual(manifest_before, load_manifest(target))

    def test_interrupted_apply_is_journaled_and_rollbackable(self) -> None:
        temporary, root, target = self.make_repo(two_skills=True)
        self.addCleanup(temporary.cleanup)
        with self.assertRaisesRegex(SyncError, "simulated interruption"):
            sync_skills(
                root,
                target,
                ["sample-skill", "second-skill"],
                apply=True,
                run_id="interrupted",
                fail_after=1,
            )
        journal_path = target / MANAGED_DIR / "runs" / "interrupted.json"
        journal = json.loads(journal_path.read_text(encoding="utf-8"))
        self.assertEqual("recovery-required", journal["status"])
        self.assertEqual(1, len(load_manifest(target)["skills"]))
        rollback_run(target, "interrupted")
        self.assertFalse((target / "sample-skill").exists())
        self.assertFalse((target / "second-skill").exists())
        self.assertEqual({}, load_manifest(target)["skills"])

    def test_deprecated_retirement_requires_flag_and_manifest_ownership(self) -> None:
        temporary, root, target = self.make_repo()
        self.addCleanup(temporary.cleanup)
        sync_skills(root, target, ["sample-skill"], apply=True, run_id="install-one")
        registry_path = root / "skills" / "registry.json"
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        registry["skills"][0]["maturity"] = "deprecated"
        registry["skills"][0]["distribution"] = {
            "standalone_archive": False,
            "stable_plugin": False,
            "public_install": False,
        }
        registry_path.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
        preview = sync_skills(root, target, None, all_skills=True, run_id="no-retire")
        self.assertEqual([], preview["operations"])
        preview = sync_skills(
            root,
            target,
            None,
            all_skills=True,
            retire_deprecated=True,
            run_id="retire-preview",
        )
        self.assertEqual("retire", preview["operations"][0]["action"])
        sync_skills(
            root,
            target,
            None,
            all_skills=True,
            apply=True,
            retire_deprecated=True,
            run_id="retire-apply",
        )
        self.assertFalse((target / "sample-skill").exists())
        self.assertEqual({}, load_manifest(target)["skills"])


if __name__ == "__main__":
    unittest.main()
