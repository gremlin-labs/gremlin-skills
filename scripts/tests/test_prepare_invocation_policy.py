from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

from prepare_invocation_policy import build_manifest, recommendation, render_report, validate_manifest  # noqa: E402
from skill_registry import load_registry  # noqa: E402


class InvocationPolicyProposalTests(unittest.TestCase):
    def make_repo(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name) / "repo"
        fixture = Path(__file__).resolve().parent / "fixtures" / "valid-repo"
        shutil.copytree(fixture, root)
        return temporary, root

    def test_read_only_skill_is_model_visible(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        registry = load_registry(root)
        manifest = build_manifest(registry)
        self.assertEqual("model-visible", manifest["skills"][0]["proposed_mode"])
        self.assertEqual([], validate_manifest(registry, manifest))
        self.assertIn("Proposal SHA-256", render_report(manifest))

    def test_source_mutating_executor_is_user_only(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        registry = load_registry(root)
        record = json.loads(json.dumps(registry.records[0]))
        record["authority"] = {"mode": "executor", "source_mutation": "task-scoped", "external_actions": "none"}
        self.assertEqual("user-only", recommendation(record)[0])

    def test_digest_tampering_fails(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        registry = load_registry(root)
        manifest = build_manifest(registry)
        manifest["proposal_sha256"] = "0" * 64
        errors = validate_manifest(registry, manifest)
        self.assertTrue(any("proposal digest mismatch" in error for error in errors), errors)

    def test_registry_mode_cannot_change_before_approval(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        registry = load_registry(root)
        manifest = build_manifest(registry)
        path = root / "skills" / "registry.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["skills"][0]["invocation"] = {
            "mode": "model-visible",
            "claude": "model-visible",
            "codex": "model-visible",
        }
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        errors = validate_manifest(load_registry(root), manifest)
        self.assertTrue(any("changed before owner approval" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
