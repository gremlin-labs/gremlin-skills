#!/usr/bin/env python3
"""Run every registry-declared skill-local test command without a shell."""

from __future__ import annotations

import argparse
import json
import os
import shlex
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from skill_registry import RegistryError, load_registry


ALLOWED_EXECUTABLES = {"node", "python3"}


class SkillTestError(RuntimeError):
    """Raised when a declared command cannot be executed safely."""


def _atomic_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def _arguments(command: str) -> list[str]:
    try:
        arguments = shlex.split(command)
    except ValueError as error:
        raise SkillTestError(f"cannot parse declared command: {error}") from error
    if not arguments or arguments[0] not in ALLOWED_EXECUTABLES:
        allowed = ", ".join(sorted(ALLOWED_EXECUTABLES))
        raise SkillTestError(f"declared command must use an approved no-shell executable ({allowed})")
    return arguments


def run_skill_tests(repo_root: Path, *, timeout: int = 120) -> tuple[dict[str, Any], list[str]]:
    repo_root = repo_root.resolve()
    registry = load_registry(repo_root)
    errors: list[str] = []
    results: list[dict[str, Any]] = []
    passed = failed = unavailable = suites = 0
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"

    for record in registry.promoted:
        commands = record["tests"]
        if not commands:
            results.append({"skill": record["name"], "status": "NOT_DECLARED", "commands": []})
            continue
        command_results: list[dict[str, Any]] = []
        skill_failed = False
        skill_unavailable = False
        for command in commands:
            suites += 1
            try:
                arguments = _arguments(command)
            except SkillTestError as error:
                command_results.append({"command": command, "status": "INVALID", "returncode": None})
                errors.append(f"{record['name']}: {error}")
                skill_failed = True
                continue
            if shutil.which(arguments[0]) is None:
                command_results.append({"command": command, "status": "UNAVAILABLE", "returncode": None})
                errors.append(f"{record['name']}: required runtime '{arguments[0]}' is unavailable")
                skill_unavailable = True
                continue
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
            except subprocess.TimeoutExpired:
                command_results.append({"command": command, "status": "TIMED_OUT", "returncode": None})
                errors.append(f"{record['name']}: test timed out after {timeout} seconds: {command}")
                skill_failed = True
                continue
            elapsed_ms = round((time.monotonic() - started) * 1000)
            status = "PASSED" if completed.returncode == 0 else "FAILED"
            command_results.append({
                "command": command,
                "status": status,
                "returncode": completed.returncode,
                "elapsed_ms": elapsed_ms,
            })
            if completed.returncode != 0:
                errors.append(
                    f"{record['name']}: test failed with exit code {completed.returncode}: {command}\n"
                    f"stdout:\n{completed.stdout[-4000:]}\nstderr:\n{completed.stderr[-4000:]}"
                )
                skill_failed = True
        if skill_failed:
            status = "FAILED"
            failed += 1
        elif skill_unavailable:
            status = "UNAVAILABLE"
            unavailable += 1
        else:
            status = "PASSED"
            passed += 1
        results.append({"skill": record["name"], "status": status, "commands": command_results})

    receipt = {
        "schema_version": 1,
        "runner": "gremlin-skill-tests",
        "summary": {
            "promoted_skills": len(registry.promoted),
            "declared_suites": suites,
            "skills_passed": passed,
            "skills_failed": failed,
            "skills_unavailable": unavailable,
            "skills_without_declared_suite": len(registry.promoted) - passed - failed - unavailable,
        },
        "results": results,
    }
    return receipt, errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--timeout", type=int, default=120, help="Per-command timeout in seconds.")
    parser.add_argument("--receipt", type=Path, help="Optional machine-readable receipt path.")
    args = parser.parse_args(argv)
    if args.timeout < 1:
        parser.error("--timeout must be positive")
    try:
        receipt, errors = run_skill_tests(args.repo_root, timeout=args.timeout)
        if args.receipt:
            _atomic_json(args.receipt.resolve(), receipt)
    except (OSError, RegistryError, SkillTestError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    for result in receipt["results"]:
        if result["status"] != "NOT_DECLARED":
            print(f"{result['status']:11} {result['skill']}")
    summary = receipt["summary"]
    print(
        f"Ran {summary['declared_suites']} declared suite(s): {summary['skills_passed']} skill(s) passed, "
        f"{summary['skills_failed']} failed, {summary['skills_unavailable']} unavailable; "
        f"{summary['skills_without_declared_suite']} have no skill-local suite."
    )
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
