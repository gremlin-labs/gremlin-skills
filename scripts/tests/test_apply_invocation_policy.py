from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

from apply_invocation_policy import InvocationApplyError, apply_policy  # noqa: E402
from prepare_invocation_policy import build_manifest, render_report  # noqa: E402
from skill_registry import load_registry  # noqa: E402


class InvocationPolicyApplyTests(unittest.TestCase):
    def make_repo(self) -> tuple[tempfile.TemporaryDirectory[str], Path, Path, Path]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name) / "repo"
        fixture = Path(__file__).resolve().parent / "fixtures" / "valid-repo"
        shutil.copytree(fixture, root)
        registry = load_registry(root)
        proposal = build_manifest(registry)
        manifest = root / "migrations" / "invocation-policy-v1.json"
        report = root / "agent-work" / "test" / "goalpro" / "INVOCATION-MATRIX.md"
        manifest.parent.mkdir(parents=True)
        report.parent.mkdir(parents=True)
        manifest.write_text(json.dumps(proposal, indent=2) + "\n", encoding="utf-8")
        report.write_text(render_report(proposal), encoding="utf-8")
        return temporary, root, manifest, report

    def test_exact_confirmation_applies_complete_policy(self) -> None:
        temporary, root, manifest, report = self.make_repo()
        self.addCleanup(temporary.cleanup)
        digest = json.loads(manifest.read_text(encoding="utf-8"))["proposal_sha256"]
        self.assertEqual(digest, apply_policy(root, manifest, report, f"sha256:{digest}"))
        registry = load_registry(root)
        self.assertEqual("approved", registry.data["invocation_policy"]["status"])
        self.assertEqual("model-visible", registry.records[0]["invocation"]["mode"])
        self.assertEqual("approved", json.loads(manifest.read_text(encoding="utf-8"))["status"])
        self.assertIn("Status: `approved`", report.read_text(encoding="utf-8"))

    def test_wrong_confirmation_leaves_every_file_unchanged(self) -> None:
        temporary, root, manifest, report = self.make_repo()
        self.addCleanup(temporary.cleanup)
        paths = (root / "skills" / "registry.json", manifest, report)
        before = {path: path.read_bytes() for path in paths}
        with self.assertRaisesRegex(InvocationApplyError, "confirmation must equal"):
            apply_policy(root, manifest, report, "sha256:wrong")
        self.assertEqual(before, {path: path.read_bytes() for path in paths})


if __name__ == "__main__":
    unittest.main()
