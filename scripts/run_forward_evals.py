#!/usr/bin/env python3
"""Generate the fresh-context routing queue and validate reviewable receipts."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

from skill_registry import RegistryError, load_registry


DEFAULT_PLAN = Path("evals/forward-plan.json")
DEFAULT_RECEIPTS = Path("evals/forward-receipts")
RFC3339_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
RECEIPT_FIELDS = {
    "schema_version",
    "case_id",
    "skill",
    "run_id",
    "host",
    "model",
    "started_at",
    "fresh_context",
    "context_sources",
    "result",
    "evidence",
    "artifacts",
    "reviewed_by",
    "notes",
}


class ForwardEvalError(RuntimeError):
    """Raised when the evaluation plan or receipt corpus is invalid."""


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def build_plan(repo_root: Path) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    registry = load_registry(repo_root)
    triggers = _load(repo_root / "evals" / "trigger-cases.json")["cases"]
    authority = {case["skill"]: case for case in _load(repo_root / "evals" / "authority-cases.json")["cases"]}
    artifacts = {
        contract["skill"]: contract for contract in _load(repo_root / "evals" / "artifact-contracts.json")["contracts"]
    }
    modes = {record["name"]: record["invocation"]["mode"] for record in registry.promoted}
    jobs: list[dict[str, Any]] = []
    for record in registry.promoted:
        name = record["name"]
        positive = next(
            (case for case in triggers if case["category"] == "positive" and case["expected_skill"] == name),
            None,
        )
        near_miss = next(
            (case for case in triggers if case["category"] == "near-miss" and name in case["must_not_win"]),
            None,
        )
        if positive is None or near_miss is None or name not in authority or name not in artifacts:
            raise ForwardEvalError(f"cannot build complete forward queue for '{name}'")
        positive_invocation = {
            "mode": "explicit" if modes[name] == "user-only" else "implicit",
            "skill": name if modes[name] == "user-only" else None,
        }
        near_winner = near_miss["expected_skill"]
        near_invocation = {
            "mode": "explicit" if modes.get(near_winner) == "user-only" else "implicit",
            "skill": near_winner if modes.get(near_winner) == "user-only" else None,
        }
        jobs.extend([
            {
                "id": f"{name}--routing-positive",
                "skill": name,
                "kind": "routing-explicit" if modes[name] == "user-only" else "routing-positive",
                "source_case_id": positive["id"],
                "prompt": positive["prompt"],
                "invocation": positive_invocation,
                "expected": {
                    "winner": name,
                    "must_not_win": positive["must_not_win"],
                },
                "fresh_context_required": True,
            },
            {
                "id": f"{name}--routing-near-miss",
                "skill": name,
                "kind": "routing-near-miss",
                "source_case_id": near_miss["id"],
                "prompt": near_miss["prompt"],
                "invocation": near_invocation,
                "expected": {
                    "winner": near_miss["expected_skill"],
                    "must_not_win": near_miss["must_not_win"],
                },
                "fresh_context_required": True,
            },
        ])
    return {
        "schema_version": 1,
        "policy": {
            "fresh_context_per_job": True,
            "expected_result_hidden_from_agent": True,
            "fixture_repository_disposable": True,
            "independent_review_required": True,
            "host_native_explicit_invocation": True,
            "model_scope": ["routing-positive", "routing-explicit", "routing-near-miss"],
            "deterministic_scope": ["authority", "artifact"],
            "results": ["FAIL", "PARTIAL", "PASS"],
        },
        "jobs": jobs,
    }


def render_plan(repo_root: Path) -> str:
    return json.dumps(build_plan(repo_root), indent=2, ensure_ascii=False) + "\n"


def validate_receipts(
    repo_root: Path,
    plan: dict[str, Any],
    receipts_root: Path,
    *,
    require_complete: bool = False,
) -> tuple[dict[str, int], list[str]]:
    jobs = {job["id"]: job for job in plan["jobs"]}
    errors: list[str] = []
    seen: set[str] = set()
    digest_values: dict[str, set[str]] = {
        "payload_sha256": set(),
        "plan_sha256": set(),
        "harness_sha256": set(),
    }
    result_counts = {"PASS": 0, "PARTIAL": 0, "FAIL": 0, "MISSING": 0}
    for path in sorted(receipts_root.glob("*.json")) if receipts_root.is_dir() else []:
        try:
            receipt = _load(path)
        except (OSError, json.JSONDecodeError) as error:
            errors.append(f"{path.name}: {error}")
            continue
        if not isinstance(receipt, dict) or set(receipt) != RECEIPT_FIELDS:
            errors.append(f"{path.name}: fields do not match receipt schema")
            continue
        case_id = receipt["case_id"]
        job = jobs.get(case_id)
        if job is None:
            errors.append(f"{path.name}: unknown case_id '{case_id}'")
            continue
        if path.name != f"{case_id}.json":
            errors.append(f"{path.name}: filename must match case_id")
        if case_id in seen:
            errors.append(f"{path.name}: duplicate case_id '{case_id}'")
        seen.add(case_id)
        if receipt["schema_version"] != 1 or receipt["skill"] != job["skill"]:
            errors.append(f"{path.name}: identity mismatch")
        for field in ("run_id", "host", "model", "reviewed_by"):
            if not isinstance(receipt[field], str) or not receipt[field].strip():
                errors.append(f"{path.name}: {field} must be non-empty")
        if not isinstance(receipt["started_at"], str) or not RFC3339_RE.fullmatch(receipt["started_at"]):
            errors.append(f"{path.name}: started_at must be UTC RFC3339 seconds")
        if receipt["fresh_context"] is not True:
            errors.append(f"{path.name}: fresh_context must be true")
        if receipt["context_sources"] != ["fixture-repository", "installed-skill", "user-prompt"]:
            errors.append(f"{path.name}: context_sources must be the canonical leakage-safe set")
        result = receipt["result"]
        if result not in result_counts or result == "MISSING":
            errors.append(f"{path.name}: invalid result")
        else:
            result_counts[result] += 1
        for field in ("evidence", "artifacts"):
            value = receipt[field]
            if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
                errors.append(f"{path.name}: {field} must be a string array")
        if not receipt["evidence"]:
            errors.append(f"{path.name}: evidence must not be empty")
        evidence = receipt["evidence"] if isinstance(receipt["evidence"], list) else []
        selections = [item.split("=", 1)[1] for item in evidence if item.startswith("selected_skill=")]
        if len(selections) != 1:
            errors.append(f"{path.name}: evidence must contain exactly one selected_skill entry")
        else:
            selected = selections[0]
            expected = job["expected"]
            expected_result = (
                "PASS"
                if selected == expected["winner"] and selected not in expected["must_not_win"]
                else "FAIL"
            )
            if receipt["result"] != expected_result:
                errors.append(f"{path.name}: result disagrees with the recorded selection and current plan")
        for digest_name in ("payload_sha256", "plan_sha256", "harness_sha256"):
            matches = [item for item in evidence if item.startswith(f"{digest_name}=")]
            if len(matches) != 1 or not re.fullmatch(rf"{digest_name}=[0-9a-f]{{64}}", matches[0]):
                errors.append(f"{path.name}: evidence must contain one valid {digest_name} entry")
            else:
                digest_values[digest_name].add(matches[0].split("=", 1)[1])
        if not isinstance(receipt["notes"], str):
            errors.append(f"{path.name}: notes must be a string")
        rendered = json.dumps(receipt)
        local_prefixes = (
            str(repo_root),
            str(repo_root.resolve()),
            "/Users/",
            "/home/",
            "/private/var/",
            "/var/folders/",
            "/tmp/",
        )
        if any(prefix in rendered for prefix in local_prefixes):
            errors.append(f"{path.name}: receipt exposes an absolute local path")
    missing = set(jobs) - seen
    result_counts["MISSING"] = len(missing)
    for digest_name, values in digest_values.items():
        if len(values) > 1:
            errors.append(f"forward receipts mix multiple {digest_name} values")
    plan_path = repo_root / DEFAULT_PLAN
    harness_path = repo_root / "scripts" / "execute_forward_evals.py"
    current_digests = {
        "plan_sha256": hashlib.sha256(plan_path.read_bytes()).hexdigest() if plan_path.is_file() else None,
        "harness_sha256": hashlib.sha256(harness_path.read_bytes()).hexdigest() if harness_path.is_file() else None,
    }
    for digest_name, current in current_digests.items():
        values = digest_values[digest_name]
        if current is not None and values and values != {current}:
            errors.append(f"forward receipts do not match the current {digest_name}")
    if require_complete and missing:
        errors.append(f"forward receipts incomplete: {len(missing)} of {len(jobs)} job(s) missing")
    if require_complete and (result_counts["FAIL"] or result_counts["PARTIAL"]):
        errors.append(
            "forward receipts are not promotion-ready: "
            f"{result_counts['FAIL']} FAIL and {result_counts['PARTIAL']} PARTIAL"
        )
    return result_counts, errors


def _atomic_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(content, encoding="utf-8")
    temporary.replace(path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--plan", type=Path)
    parser.add_argument("--receipts", type=Path)
    parser.add_argument("--write-plan", action="store_true")
    parser.add_argument("--check-plan", action="store_true")
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args(argv)
    if args.write_plan and args.check_plan:
        parser.error("choose --write-plan or --check-plan")
    repo_root = args.repo_root.resolve()
    plan_path = (args.plan or repo_root / DEFAULT_PLAN).resolve()
    receipts_root = (args.receipts or repo_root / DEFAULT_RECEIPTS).resolve()
    try:
        expected = render_plan(repo_root)
        if args.write_plan:
            _atomic_text(plan_path, expected)
        elif plan_path.read_text(encoding="utf-8") != expected:
            raise ForwardEvalError("forward evaluation plan is stale; run with --write-plan")
        plan = json.loads(expected)
        counts, errors = validate_receipts(
            repo_root,
            plan,
            receipts_root,
            require_complete=args.require_complete,
        )
    except (OSError, json.JSONDecodeError, RegistryError, ForwardEvalError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    action = "Wrote and validated" if args.write_plan else "Validated"
    print(
        f"{action} {len(plan['jobs'])} fresh-context jobs; receipts: "
        f"{counts['PASS']} PASS, {counts['PARTIAL']} PARTIAL, {counts['FAIL']} FAIL, {counts['MISSING']} missing."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
