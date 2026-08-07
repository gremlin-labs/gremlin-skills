#!/usr/bin/env python3
"""Run the deterministic repository release-candidate gate and write a safe receipt."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


DEFAULT_RECEIPT = Path("dist/validation/validation-receipt.json")


def validation_commands() -> list[tuple[str, list[str]]]:
    return [
        ("root-tests", ["python3", "-m", "unittest", "discover", "-s", "scripts/tests", "-p", "test_*.py"]),
        ("generated-docs", ["python3", "scripts/generate_docs.py"]),
        ("materialized-contracts", ["python3", "scripts/materialize_contracts.py", "--check"]),
        ("generated-authority-cases", ["python3", "scripts/generate_authority_cases.py", "--check"]),
        ("layout-migration", ["python3", "scripts/prepare_skill_layout.py", "--check"]),
        ("layout-apply-preflight", ["python3", "scripts/apply_skill_layout.py"]),
        ("invocation-proposal", ["python3", "scripts/prepare_invocation_policy.py", "--check"]),
        ("host-metadata", ["python3", "scripts/generate_plugin_manifests.py", "--check"]),
        ("registry", ["python3", "scripts/validate_registry.py"]),
        ("public-docs", ["python3", "scripts/validate_docs.py"]),
        ("public-release-safety", ["python3", "scripts/validate_public_release.py"]),
        (
            "public-clean-snapshot",
            [
                "python3",
                "scripts/prepare_public_snapshot.py",
                "--receipt",
                "dist/validation/public-snapshot-receipt.json",
            ],
        ),
        ("skill-sources", ["python3", "scripts/validate_skills.py"]),
        ("evaluations", ["python3", "scripts/validate_evals.py"]),
        (
            "forward-evaluations",
            ["python3", "scripts/run_forward_evals.py", "--check-plan", "--require-complete"],
        ),
        (
            "coexistence-fixture",
            [
                "python3",
                "scripts/smoke_test_coexistence.py",
                "--receipt",
                "dist/validation/coexistence-fixture-receipt.json",
            ],
        ),
        (
            "skill-local-tests",
            [
                "python3",
                "scripts/run_skill_tests.py",
                "--receipt",
                "dist/validation/skill-test-receipt.json",
            ],
        ),
        ("packages-build", ["python3", "scripts/package_skills.py", "--clean"]),
        ("packages-extracted", ["python3", "scripts/validate_packages.py"]),
        (
            "plugins-build",
            ["python3", "scripts/generate_plugin_manifests.py", "--write", "--clean"],
        ),
        ("plugins-validated", ["python3", "scripts/validate_plugins.py"]),
        ("version-sync", ["node", "scripts/sync-plugin-version.mjs", "--check"]),
        ("whitespace", ["git", "diff", "--check"]),
    ]


def run_commands(
    repo_root: Path,
    commands: list[tuple[str, list[str]]],
    *,
    timeout: int = 300,
) -> tuple[dict[str, Any], list[str]]:
    repo_root = repo_root.resolve()
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    results: list[dict[str, Any]] = []
    errors: list[str] = []
    for check_id, arguments in commands:
        started = time.monotonic()
        try:
            completed = subprocess.run(
                arguments,
                cwd=repo_root,
                env=environment,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )
            elapsed_ms = round((time.monotonic() - started) * 1000)
            status = "PASSED" if completed.returncode == 0 else "FAILED"
            results.append({
                "id": check_id,
                "command": arguments,
                "status": status,
                "returncode": completed.returncode,
                "elapsed_ms": elapsed_ms,
            })
            if completed.returncode != 0:
                errors.append(
                    f"{check_id} failed with exit code {completed.returncode}\n"
                    f"stdout:\n{completed.stdout[-6000:]}\nstderr:\n{completed.stderr[-6000:]}"
                )
        except subprocess.TimeoutExpired:
            elapsed_ms = round((time.monotonic() - started) * 1000)
            results.append({
                "id": check_id,
                "command": arguments,
                "status": "TIMED_OUT",
                "returncode": None,
                "elapsed_ms": elapsed_ms,
            })
            errors.append(f"{check_id} timed out after {timeout} seconds")
    receipt = {
        "schema_version": 1,
        "runner": "gremlin-validation",
        "status": "PASSED" if not errors else "FAILED",
        "summary": {
            "checks": len(results),
            "passed": sum(result["status"] == "PASSED" for result in results),
            "failed": sum(result["status"] != "PASSED" for result in results),
        },
        "checks": results,
    }
    return receipt, errors


def write_receipt(path: Path, receipt: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--timeout", type=int, default=300, help="Per-check timeout in seconds.")
    args = parser.parse_args(argv)
    if args.timeout < 1:
        parser.error("--timeout must be positive")
    repo_root = args.repo_root.resolve()
    receipt_path = (args.receipt or repo_root / DEFAULT_RECEIPT).resolve()
    try:
        receipt, errors = run_commands(repo_root, validation_commands(), timeout=args.timeout)
        write_receipt(receipt_path, receipt)
    except OSError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    for result in receipt["checks"]:
        print(f"{result['status']:9} {result['id']} ({result['elapsed_ms']} ms)")
    print(
        f"Validation {receipt['status']}: {receipt['summary']['passed']}/{receipt['summary']['checks']} checks passed; "
        f"receipt {receipt_path}."
    )
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
