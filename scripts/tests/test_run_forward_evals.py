from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

from run_forward_evals import build_plan, validate_receipts  # noqa: E402


class ForwardEvaluationTests(unittest.TestCase):
    def make_repo(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name) / "repo"
        fixture = Path(__file__).resolve().parent / "fixtures" / "valid-repo"
        shutil.copytree(fixture, root)
        evals = root / "evals"
        evals.mkdir()
        triggers = {
            "cases": [
                {"id": "positive", "category": "positive", "prompt": "Audit this sample.", "expected_skill": "sample-skill", "must_not_win": ["other-skill"], "rationale": "fixture"},
                {"id": "near", "category": "near-miss", "prompt": "Do something else.", "expected_skill": "other-skill", "must_not_win": ["sample-skill"], "rationale": "fixture"},
            ]
        }
        authority = {"cases": [{
            "id": "sample-authority",
            "skill": "sample-skill",
            "prompt": "Audit this sample.",
            "expected_authority": {"mode": "read-only", "source_mutation": "never", "external_actions": "none"},
            "allowed_actions": ["Inspect."],
            "prohibited_actions": ["Edit."],
            "required_gates": ["Remain read-only."],
            "failure_if": ["Edited."],
        }]}
        artifacts = {"contracts": [{
            "skill": "sample-skill",
            "output_root": "agent-work/{slug}/sample-skill/",
            "files": [{"path": "MAIN.md", "required": True, "headings": ["Goal"]}],
        }]}
        for name, data in (("trigger-cases.json", triggers), ("authority-cases.json", authority), ("artifact-contracts.json", artifacts)):
            (evals / name).write_text(json.dumps(data), encoding="utf-8")
        return temporary, root

    def test_plan_contains_two_routing_jobs_per_promoted_skill(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        plan = build_plan(root)
        self.assertEqual(2, len(plan["jobs"]))
        self.assertTrue(all(job["fresh_context_required"] for job in plan["jobs"]))
        self.assertTrue(all(job["invocation"]["mode"] == "implicit" for job in plan["jobs"]))

    def test_user_only_jobs_require_explicit_positive_invocation(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        path = root / "skills" / "registry.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["invocation_policy"]["status"] = "approved"
        data["skills"][0]["invocation"] = {
            "mode": "user-only",
            "claude": "user-only",
            "codex": "user-only",
        }
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        jobs = build_plan(root)["jobs"]
        by_kind = {job["kind"]: job for job in jobs}
        self.assertEqual("explicit", by_kind["routing-explicit"]["invocation"]["mode"])
        self.assertEqual("sample-skill", by_kind["routing-explicit"]["invocation"]["skill"])
        self.assertEqual("implicit", by_kind["routing-near-miss"]["invocation"]["mode"])

    def test_complete_receipt_is_accepted_and_missing_is_counted(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        plan = build_plan(root)
        receipts = root / "receipts"
        receipts.mkdir()
        job = plan["jobs"][0]
        receipt = {
            "schema_version": 1,
            "case_id": job["id"],
            "skill": job["skill"],
            "run_id": "fixture-1",
            "host": "fixture-host",
            "model": "fixture-model",
            "started_at": "2026-08-06T23:00:00Z",
            "fresh_context": True,
            "context_sources": ["fixture-repository", "installed-skill", "user-prompt"],
            "result": "PASS",
            "evidence": [
                "selected_skill=sample-skill",
                f"payload_sha256={'1' * 64}",
                f"plan_sha256={'2' * 64}",
                f"harness_sha256={'3' * 64}",
            ],
            "artifacts": [],
            "reviewed_by": "fixture-reviewer",
            "notes": "",
        }
        (receipts / f"{job['id']}.json").write_text(json.dumps(receipt), encoding="utf-8")
        counts, errors = validate_receipts(root, plan, receipts)
        self.assertEqual([], errors)
        self.assertEqual(1, counts["PASS"])
        self.assertEqual(1, counts["MISSING"])
        _, strict_errors = validate_receipts(root, plan, receipts, require_complete=True)
        self.assertTrue(any("incomplete" in error for error in strict_errors), strict_errors)

    def test_receipt_rejects_context_leakage(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        plan = build_plan(root)
        receipts = root / "receipts"
        receipts.mkdir()
        job = plan["jobs"][0]
        receipt = {
            "schema_version": 1,
            "case_id": job["id"],
            "skill": job["skill"],
            "run_id": "fixture-1",
            "host": "fixture-host",
            "model": "fixture-model",
            "started_at": "2026-08-06T23:00:00Z",
            "fresh_context": False,
            "context_sources": ["expected-answer"],
            "result": "PASS",
            "evidence": [
                "selected_skill=sample-skill",
                f"payload_sha256={'1' * 64}",
                f"plan_sha256={'2' * 64}",
                f"harness_sha256={'3' * 64}",
                f"Read {root}/expected.md",
            ],
            "artifacts": [],
            "reviewed_by": "fixture-reviewer",
            "notes": "",
        }
        (receipts / f"{job['id']}.json").write_text(json.dumps(receipt), encoding="utf-8")
        _, errors = validate_receipts(root, plan, receipts)
        self.assertTrue(any("fresh_context" in error for error in errors), errors)
        self.assertTrue(any("absolute local path" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
