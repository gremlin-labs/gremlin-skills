from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

from prepare_skill_layout import build_manifest, validate_manifest  # noqa: E402
from skill_registry import load_registry  # noqa: E402


class SkillLayoutMigrationTests(unittest.TestCase):
    def make_repo(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name) / "repo"
        fixture = Path(__file__).resolve().parent / "fixtures" / "valid-repo"
        shutil.copytree(fixture, root)
        return temporary, root

    def write_registry(self, root: Path, data: dict) -> None:
        path = root / "skills" / "registry.json"
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    def test_current_flat_layout_builds_a_digest_bound_proposal(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        registry = load_registry(root)
        manifest = build_manifest(root, registry)
        state, errors = validate_manifest(root, registry, manifest)
        self.assertEqual("pre-move", state)
        self.assertEqual([], errors)
        self.assertEqual("awaiting-owner-confirmation", manifest["status"])
        self.assertEqual(64, len(manifest["proposal_sha256"]))
        self.assertIn("destination_tree_sha256", manifest["moves"][0])

    def test_proposal_digest_tampering_fails(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        registry = load_registry(root)
        manifest = build_manifest(root, registry)
        manifest["proposal_sha256"] = "0" * 64
        _, errors = validate_manifest(root, registry, manifest)
        self.assertTrue(any("proposal digest mismatch" in error for error in errors), errors)

    def test_source_tree_change_fails(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        registry = load_registry(root)
        manifest = build_manifest(root, registry)
        skill = root / "skills" / "sample-skill" / "SKILL.md"
        skill.write_text(skill.read_text(encoding="utf-8") + "\nDrift.\n", encoding="utf-8")
        _, errors = validate_manifest(root, registry, manifest)
        self.assertTrue(any("active tree digest or file count changed" in error for error in errors), errors)

    def test_completed_post_move_manifest_allows_normal_skill_maintenance(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        registry_data = json.loads((root / "skills" / "registry.json").read_text(encoding="utf-8"))
        manifest = build_manifest(root, load_registry(root))
        move = manifest["moves"][0]
        source = root / move["source"]
        destination = root / move["destination"]
        destination.parent.mkdir(parents=True)
        source.rename(destination)
        registry_data["skills"][0]["path"] = move["destination"]
        registry_data["category_model"]["status"] = "approved"
        manifest["category_model"]["status"] = "approved"
        manifest["status"] = "completed"
        self.write_registry(root, registry_data)
        skill = destination / "SKILL.md"
        skill.write_text(skill.read_text(encoding="utf-8") + "\nMaintained after migration.\n", encoding="utf-8")
        state, errors = validate_manifest(root, load_registry(root), manifest)
        self.assertEqual("post-move", state)
        self.assertEqual([], errors)

    def test_move_and_reverse_move_preserve_exact_tree_digest(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        registry = load_registry(root)
        registry_data = json.loads((root / "skills" / "registry.json").read_text(encoding="utf-8"))
        manifest = build_manifest(root, registry)
        proposal_digest = manifest["proposal_sha256"]
        move = manifest["moves"][0]
        source = root / move["source"]
        destination = root / move["destination"]

        destination.parent.mkdir(parents=True)
        source.rename(destination)
        registry_data["skills"][0]["path"] = move["destination"]
        registry_data["category_model"]["status"] = "approved"
        manifest["category_model"]["status"] = "approved"
        manifest["status"] = "ready"
        self.write_registry(root, registry_data)
        moved_registry = load_registry(root)
        state, errors = validate_manifest(root, moved_registry, manifest)
        self.assertEqual("post-move", state)
        self.assertEqual([], errors)

        destination.rename(source)
        destination.parent.rmdir()
        registry_data["skills"][0]["path"] = move["source"]
        registry_data["category_model"]["status"] = "proposed"
        manifest["category_model"]["status"] = "proposed"
        manifest["status"] = "awaiting-owner-confirmation"
        self.write_registry(root, registry_data)
        restored_registry = load_registry(root)
        state, errors = validate_manifest(root, restored_registry, manifest)
        self.assertEqual("pre-move", state)
        self.assertEqual([], errors)
        self.assertEqual(proposal_digest, build_manifest(root, restored_registry)["proposal_sha256"])

    def test_approval_status_can_change_without_changing_proposal_digest(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        registry = load_registry(root)
        pending = build_manifest(root, registry)
        registry_data = json.loads((root / "skills" / "registry.json").read_text(encoding="utf-8"))
        registry_data["category_model"]["status"] = "approved"
        self.write_registry(root, registry_data)
        approved = build_manifest(root, load_registry(root))
        self.assertEqual("ready", approved["status"])
        self.assertEqual(pending["proposal_sha256"], approved["proposal_sha256"])

    def test_cross_category_markdown_link_is_bound_to_destination_digest(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
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
        registry_data = json.loads((root / "skills" / "registry.json").read_text(encoding="utf-8"))
        registry_data["category_model"]["values"].append("experience")
        beta_record = json.loads(json.dumps(registry_data["skills"][0]))
        beta_record["name"] = "beta"
        beta_record["category"] = "experience"
        beta_record["path"] = "skills/beta"
        beta_record["output_root"] = "agent-work/{slug}/beta/"
        beta_record["public_docs"]["path"] = "docs/skills/beta.md"
        registry_data["skills"].insert(0, beta_record)
        self.write_registry(root, registry_data)

        manifest = build_manifest(root, load_registry(root))
        self.assertEqual(1, len(manifest["markdown_link_rewrites"]))
        rewrite = manifest["markdown_link_rewrites"][0]
        self.assertEqual("../beta/SKILL.md", rewrite["before"])
        self.assertEqual("../../experience/beta/SKILL.md", rewrite["after"])
        sample_move = next(move for move in manifest["moves"] if move["name"] == "sample-skill")
        self.assertNotEqual(sample_move["source_tree_sha256"], sample_move["destination_tree_sha256"])


if __name__ == "__main__":
    unittest.main()
