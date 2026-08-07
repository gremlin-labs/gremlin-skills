#!/usr/bin/env python3
"""Execute the generated routing queue in isolated, fresh Codex contexts."""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from run_forward_evals import DEFAULT_PLAN, DEFAULT_RECEIPTS, ForwardEvalError, build_plan


DEFAULT_RAW_ROOT = Path("dist/validation/forward-evals")
DEFAULT_MODEL = "gpt-5.6-terra"
OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "selected_skill": {"type": ["string", "null"]},
        "rationale": {"type": "string"},
    },
    "required": ["selected_skill", "rationale"],
    "additionalProperties": False,
}


def routing_prompt(job: dict[str, Any]) -> str:
    invocation = job["invocation"]
    explicit = ""
    if invocation["mode"] == "explicit":
        explicit = f"The user explicitly invoked ${invocation['skill']}.\n"
    return (
        "This is a bounded skill-routing evaluation. Do not inspect files, call tools, "
        "modify the workspace, execute the request, or ask follow-up questions. Select one installed "
        "skill that should own the user request, or return null when no installed skill owns it. "
        "Return only the required JSON.\n"
        f"{explicit}"
        "User request:\n"
        f"{job['prompt']}"
    )


def classify(job: dict[str, Any], selected_skill: str) -> str:
    expected = job["expected"]
    if selected_skill != expected["winner"]:
        return "FAIL"
    if selected_skill in expected["must_not_win"]:
        return "FAIL"
    return "PASS"


def tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        relative = path.relative_to(root).as_posix().encode("utf-8")
        content = path.read_bytes()
        digest.update(len(relative).to_bytes(4, "big"))
        digest.update(relative)
        digest.update(len(content).to_bytes(8, "big"))
        digest.update(content)
    return digest.hexdigest()


def _atomic_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def _codex_version(executable: str) -> str:
    completed = subprocess.run(
        [executable, "--version"],
        capture_output=True,
        text=True,
        timeout=15,
        check=False,
    )
    if completed.returncode != 0:
        raise ForwardEvalError("cannot determine Codex CLI version")
    return completed.stdout.strip()


def execute_job(
    job: dict[str, Any],
    *,
    payload: Path,
    payload_sha256: str,
    plan_sha256: str,
    harness_sha256: str,
    auth_source: Path,
    receipts_root: Path,
    raw_root: Path,
    executable: str,
    host: str,
    model: str,
    timeout: int,
) -> tuple[str, str]:
    run_id = str(uuid.uuid4())
    started_at = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    selected_skill = ""
    reason = ""
    exit_code: int | None = None
    response = ""
    error_label = ""
    with tempfile.TemporaryDirectory(prefix="gremlin-forward-eval-") as temporary:
        root = Path(temporary)
        codex_home = root / ".codex"
        fixture = root / "fixture"
        installed = fixture / ".agents" / "skills"
        codex_home.mkdir(parents=True)
        installed.parent.mkdir(parents=True)
        shutil.copy2(auth_source, codex_home / "auth.json")
        os.chmod(codex_home / "auth.json", 0o600)
        shutil.copytree(payload, installed)
        schema_path = root / "output-schema.json"
        schema_path.write_text(json.dumps(OUTPUT_SCHEMA), encoding="utf-8")
        output_path = root / "result.json"
        environment = os.environ.copy()
        for key in list(environment):
            if key.startswith("CODEX_"):
                environment.pop(key)
        environment["HOME"] = str(root)
        environment["CODEX_HOME"] = str(codex_home)
        command = [
            executable,
            "-a",
            "never",
            "exec",
            "--ignore-user-config",
            "--ignore-rules",
            "--ephemeral",
            "--sandbox",
            "read-only",
            "--skip-git-repo-check",
            "-C",
            str(fixture),
            "--model",
            model,
            "-c",
            'model_reasoning_effort="low"',
            "--output-schema",
            str(schema_path),
            "--output-last-message",
            str(output_path),
            routing_prompt(job),
        ]
        try:
            completed = subprocess.run(
                command,
                stdin=subprocess.DEVNULL,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
                env=environment,
            )
            exit_code = completed.returncode
            response = output_path.read_text(encoding="utf-8") if output_path.is_file() else ""
            raw = {
                "case_id": job["id"],
                "run_id": run_id,
                "returncode": completed.returncode,
                "stdout": completed.stdout,
                "stderr": completed.stderr,
                "response": response,
            }
            _atomic_json(raw_root / f"{job['id']}.json", raw)
            if completed.returncode == 0:
                parsed = json.loads(response)
                selected = parsed["selected_skill"]
                selected_skill = selected.strip() if isinstance(selected, str) else "none"
                reason = parsed["rationale"].strip()
            else:
                error_label = "codex-process-failed"
        except subprocess.TimeoutExpired:
            error_label = "codex-process-timed-out"
        except (json.JSONDecodeError, KeyError, TypeError, OSError):
            error_label = "structured-response-invalid"

    result = classify(job, selected_skill) if not error_label else "FAIL"
    response_digest = hashlib.sha256(response.encode("utf-8")).hexdigest()
    evidence = [
        f"invocation={job['invocation']['mode']}",
        f"selected_skill={selected_skill or 'none'}",
        f"response_sha256={response_digest}",
        f"process_exit_code={exit_code if exit_code is not None else 'none'}",
        f"payload_sha256={payload_sha256}",
        f"plan_sha256={plan_sha256}",
        f"harness_sha256={harness_sha256}",
    ]
    if error_label:
        evidence.append(f"error={error_label}")
    receipt = {
        "schema_version": 1,
        "case_id": job["id"],
        "skill": job["skill"],
        "run_id": run_id,
        "host": host,
        "model": model,
        "started_at": started_at,
        "fresh_context": True,
        "context_sources": ["fixture-repository", "installed-skill", "user-prompt"],
        "result": result,
        "evidence": evidence,
        "artifacts": [],
        "reviewed_by": "forward-routing-harness-v1",
        "notes": reason[:500] if result != "PASS" else "",
    }
    _atomic_json(receipts_root / f"{job['id']}.json", receipt)
    return job["id"], result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--receipts", type=Path)
    parser.add_argument("--raw-root", type=Path)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--timeout", type=int, default=75)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--case-id", action="append", default=[])
    parser.add_argument("--codex", default="codex")
    args = parser.parse_args(argv)
    repo_root = args.repo_root.resolve()
    receipts_root = (args.receipts or repo_root / DEFAULT_RECEIPTS).resolve()
    raw_root = (args.raw_root or repo_root / DEFAULT_RAW_ROOT).resolve()
    payload = repo_root / "dist" / "plugins" / "codex" / "gremlin-skills" / "skills"
    auth_source = Path.home() / ".codex" / "auth.json"
    if args.workers < 1 or args.timeout < 1 or (args.limit is not None and args.limit < 1):
        parser.error("workers, timeout, and limit must be positive")
    try:
        expected_plan = build_plan(repo_root)
        plan_path = repo_root / DEFAULT_PLAN
        if json.loads(plan_path.read_text(encoding="utf-8")) != expected_plan:
            raise ForwardEvalError("forward plan is stale; regenerate it before execution")
        if not payload.is_dir():
            raise ForwardEvalError("generated flat Codex skill payload is missing")
        if not auth_source.is_file():
            raise ForwardEvalError("Codex authentication is unavailable")
        executable = shutil.which(args.codex)
        if executable is None:
            raise ForwardEvalError("Codex CLI is unavailable")
        version = _codex_version(executable)
        payload_sha256 = tree_digest(payload)
        plan_sha256 = hashlib.sha256(plan_path.read_bytes()).hexdigest()
        harness_sha256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        jobs = expected_plan["jobs"]
        if args.case_id:
            selected = set(args.case_id)
            jobs = [job for job in jobs if job["id"] in selected]
            missing = selected - {job["id"] for job in jobs}
            if missing:
                raise ForwardEvalError(f"unknown case id(s): {', '.join(sorted(missing))}")
        if args.limit is not None:
            jobs = jobs[: args.limit]
        if not jobs:
            raise ForwardEvalError("no forward jobs selected")
        results: list[tuple[str, str]] = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
            futures = [
                executor.submit(
                    execute_job,
                    job,
                    payload=payload,
                    payload_sha256=payload_sha256,
                    plan_sha256=plan_sha256,
                    harness_sha256=harness_sha256,
                    auth_source=auth_source,
                    receipts_root=receipts_root,
                    raw_root=raw_root,
                    executable=executable,
                    host=version,
                    model=args.model,
                    timeout=args.timeout,
                )
                for job in jobs
            ]
            for future in concurrent.futures.as_completed(futures):
                case_id, result = future.result()
                results.append((case_id, result))
                print(f"{result:7} {case_id}")
    except (OSError, json.JSONDecodeError, ForwardEvalError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    failures = sum(result != "PASS" for _, result in results)
    print(f"Executed {len(results)} isolated routing job(s): {len(results) - failures} PASS, {failures} FAIL.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
