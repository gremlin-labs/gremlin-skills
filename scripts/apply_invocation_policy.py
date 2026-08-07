#!/usr/bin/env python3
"""Apply an approved invocation proposal to the canonical registry atomically."""

from __future__ import annotations

import argparse
import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

from prepare_invocation_policy import DEFAULT_MANIFEST, DEFAULT_REPORT, render_report, validate_manifest
from skill_registry import RegistryError, load_registry, validate_registry_data


class InvocationApplyError(RuntimeError):
    """Raised when an invocation proposal cannot be applied safely."""


def _atomic_bytes(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_bytes(payload)
    temporary.replace(path)


def _proposal(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise InvocationApplyError(f"{path}: {error}") from error
    if not isinstance(data, dict):
        raise InvocationApplyError(f"{path}: expected a JSON object")
    return data


def proposed_registry_data(registry_data: dict[str, Any], proposal: dict[str, Any]) -> dict[str, Any]:
    modes = {
        record["name"]: record["proposed_mode"]
        for record in proposal.get("skills", [])
        if isinstance(record, dict) and isinstance(record.get("name"), str)
    }
    expected_names = {record["name"] for record in registry_data["skills"] if record["maturity"] == "promoted"}
    if set(modes) != expected_names:
        missing = sorted(expected_names - set(modes))
        extra = sorted(set(modes) - expected_names)
        details = []
        if missing:
            details.append(f"missing: {', '.join(missing)}")
        if extra:
            details.append(f"extra: {', '.join(extra)}")
        raise InvocationApplyError(f"proposal skill inventory mismatch ({'; '.join(details)})")

    updated = deepcopy(registry_data)
    updated["invocation_policy"]["status"] = "approved"
    for record in updated["skills"]:
        if record["maturity"] != "promoted":
            continue
        mode = modes[record["name"]]
        record["invocation"] = {"mode": mode, "claude": mode, "codex": mode}
    return updated


def apply_policy(repo_root: Path, manifest_path: Path, report_path: Path, confirmation: str) -> str:
    repo_root = repo_root.resolve()
    registry = load_registry(repo_root)
    proposal = _proposal(manifest_path)
    errors = validate_manifest(registry, proposal)
    if errors:
        raise InvocationApplyError("proposal preflight failed: " + "; ".join(errors))

    digest = proposal.get("proposal_sha256")
    expected_confirmation = f"sha256:{digest}"
    if confirmation != expected_confirmation:
        raise InvocationApplyError(f"confirmation must equal {expected_confirmation}")

    updated_registry = proposed_registry_data(registry.data, proposal)
    registry_errors = validate_registry_data(updated_registry, repo_root)
    if registry_errors:
        raise InvocationApplyError("updated registry is invalid: " + "; ".join(registry_errors))

    updated_proposal = deepcopy(proposal)
    updated_proposal["status"] = "approved"
    registry_bytes = json.dumps(updated_registry, indent=2, ensure_ascii=False).encode("utf-8") + b"\n"
    proposal_bytes = json.dumps(updated_proposal, indent=2, ensure_ascii=False).encode("utf-8") + b"\n"
    report_bytes = render_report(updated_proposal).encode("utf-8")
    paths = (registry.path, manifest_path, report_path)
    originals = {path: path.read_bytes() for path in paths}
    try:
        _atomic_bytes(registry.path, registry_bytes)
        _atomic_bytes(manifest_path, proposal_bytes)
        _atomic_bytes(report_path, report_bytes)
        approved_registry = load_registry(repo_root)
        post_errors = validate_manifest(approved_registry, updated_proposal)
        if post_errors:
            raise InvocationApplyError("post-apply validation failed: " + "; ".join(post_errors))
    except Exception:
        for path, payload in originals.items():
            _atomic_bytes(path, payload)
        raise
    return str(digest)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--apply", action="store_true", help="Apply the proposal after exact digest confirmation.")
    parser.add_argument("--confirm", default="", help="Exact value sha256:{proposal_sha256}.")
    args = parser.parse_args(argv)
    repo_root = args.repo_root.resolve()
    manifest = (args.manifest or repo_root / DEFAULT_MANIFEST).resolve()
    report = (args.report or repo_root / DEFAULT_REPORT).resolve()
    try:
        registry = load_registry(repo_root)
        proposal = _proposal(manifest)
        errors = validate_manifest(registry, proposal)
        if errors:
            raise InvocationApplyError("proposal preflight failed: " + "; ".join(errors))
        digest = proposal["proposal_sha256"]
        if not args.apply:
            print(f"Dry run: invocation proposal sha256:{digest} is valid; no files changed.")
            return 0
        applied = apply_policy(repo_root, manifest, report, args.confirm)
    except (InvocationApplyError, RegistryError, OSError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Applied invocation proposal sha256:{applied} to the canonical registry.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
