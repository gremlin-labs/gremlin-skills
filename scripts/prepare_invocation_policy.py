#!/usr/bin/env python3
"""Generate and validate the owner-reviewable Gremlin invocation proposal."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from skill_registry import RegistryError, SkillRegistry, load_registry


DEFAULT_MANIFEST = Path("migrations/invocation-policy-v1.json")
DEFAULT_REPORT = Path("migrations/invocation-policy-v1.md")
REQUIRED_DEPENDENCY_USES = {
    ("audit-plan", "audit-compare"): "reference",
    ("brainstormpro", "planpro"): "handoff",
    ("email-lifecycle-audit", "email-lifecycle-strategy"): "handoff",
    ("email-lifecycle-strategy", "prose-humanizer"): "embedded",
    ("feature-goal", "goalpro"): "reference",
    ("landing-page", "prose-humanizer"): "embedded",
    ("landing-page", "seo-strategy"): "context",
    ("onboarding-audit", "onboarding-direction"): "handoff",
    ("onboarding-direction", "prose-humanizer"): "embedded",
    ("prose-humanizer", "seo-strategy"): "context",
    ("seo-content", "prose-humanizer"): "embedded",
    ("seo-content", "seo-strategy"): "context",
}


class InvocationProposalError(RuntimeError):
    """Raised when the proposal cannot be generated from authoritative state."""


def recommendation(record: dict[str, Any]) -> tuple[str, str]:
    authority = record["authority"]
    if authority["mode"] == "read-only":
        return (
            "model-visible",
            "Read-only source workflow with routing fixtures; implicit selection grants no source mutation or external action.",
        )
    if record["name"] == "prose-humanizer":
        return (
            "model-visible",
            "Bounded task-scoped transformation with no external action; useful as an explicitly embedded primitive.",
        )
    if record["name"] in {"landing-page", "seo-content"}:
        return (
            "model-visible",
            "Page specialist begins read-only, requires exact approval before source mutation, and must remain auto-discoverable for operational pipeline routing.",
        )
    if record["name"] == "compact-history":
        return (
            "user-only",
            "Housekeeping executor can relocate managed artifacts after confirmation, so the human must name it.",
        )
    if authority["external_actions"] == "approval-required":
        return (
            "user-only",
            "Workflow can change external state and retains a second action approval gate after explicit invocation.",
        )
    return (
        "user-only",
        "Executor or hybrid workflow can mutate task-scoped source after its gates, so the human must name it.",
    )


def _proposal_digest(data: dict[str, Any]) -> str:
    payload = {"policy": data["policy"], "skills": data["skills"]}
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def build_manifest(registry: SkillRegistry) -> dict[str, Any]:
    actual_required_edges = {
        (record["name"], dependency)
        for record in registry.promoted
        for dependency in record["dependencies"]["required_skills"]
    }
    missing_uses = sorted(actual_required_edges - REQUIRED_DEPENDENCY_USES.keys())
    if missing_uses:
        formatted = ", ".join(f"{owner}->{dependency}" for owner, dependency in missing_uses)
        raise InvocationProposalError(f"required dependency use is unclassified: {formatted}")

    skills: list[dict[str, Any]] = []
    proposed_modes: dict[str, str] = {}
    rationales: dict[str, str] = {}
    for record in registry.promoted:
        mode, rationale = recommendation(record)
        proposed_modes[record["name"]] = mode
        rationales[record["name"]] = rationale
    for record in registry.promoted:
        required = [
            {
                "skill": dependency,
                "use": REQUIRED_DEPENDENCY_USES[(record["name"], dependency)],
                "proposed_mode": proposed_modes[dependency],
            }
            for dependency in record["dependencies"]["required_skills"]
        ]
        skills.append({
            "name": record["name"],
            "proposed_mode": proposed_modes[record["name"]],
            "authority": record["authority"],
            "required_composition": required,
            "optional_complements": record["dependencies"]["optional_skills"],
            "rationale": rationales[record["name"]],
        })
    manifest = {
        "schema_version": 1,
        "migration": "invocation-policy-v1",
        "status": (
            "approved" if registry.data["invocation_policy"]["status"] == "approved" else "awaiting-owner-confirmation"
        ),
        "policy": {
            "model_visible": "Read-only or bounded transformation skills with strong routing evidence.",
            "user_only": "High-autonomy, source-mutating, housekeeping, publishing, or external-state workflows.",
            "authority_independent": True,
            "cross_host_parity_required": True,
        },
        "skills": skills,
    }
    manifest["proposal_sha256"] = _proposal_digest(manifest)
    return manifest


def validate_manifest(registry: SkillRegistry, data: Any) -> list[str]:
    errors: list[str] = []
    fields = {"schema_version", "migration", "status", "policy", "skills", "proposal_sha256"}
    if not isinstance(data, dict) or set(data) != fields:
        return ["invocation proposal: fields do not match schema"]
    if data["schema_version"] != 1 or data["migration"] != "invocation-policy-v1":
        errors.append("invocation proposal: identity mismatch")
    try:
        expected = build_manifest(registry)
    except InvocationProposalError as error:
        return [str(error)]
    if data["proposal_sha256"] != _proposal_digest(data):
        errors.append("invocation proposal: proposal digest mismatch")
    if data["policy"] != expected["policy"] or data["skills"] != expected["skills"]:
        errors.append("invocation proposal: recommendation matrix drift")
    if data["status"] != expected["status"]:
        errors.append("invocation proposal: status disagrees with registry approval state")

    expected_modes = {record["name"]: record["proposed_mode"] for record in expected["skills"]}
    policy_status = registry.data["invocation_policy"]["status"]
    for record in registry.promoted:
        invocation = record["invocation"]
        actual = {invocation["mode"], invocation["claude"], invocation["codex"]}
        if policy_status == "pending-owner-review":
            if actual != {"pending-owner-review"}:
                errors.append(f"invocation proposal: {record['name']} changed before owner approval")
        elif actual != {expected_modes[record["name"]]}:
            errors.append(f"invocation proposal: {record['name']} does not match the approved proposal")
    return errors


def render_report(data: dict[str, Any]) -> str:
    counts: dict[str, int] = {"model-visible": 0, "user-only": 0}
    for record in data["skills"]:
        counts[record["proposed_mode"]] += 1
    registry_status = (
        "- Public registry and host metadata match this approved matrix."
        if data["status"] == "approved"
        else "- Public registry and host metadata remain unchanged until this complete matrix is approved."
    )
    lines = [
        "# Invocation policy owner review",
        "",
        f"- Status: `{data['status']}`",
        f"- Proposal SHA-256: `{data['proposal_sha256']}`",
        f"- Recommendation: {counts['model-visible']} model-visible; {counts['user-only']} user-only",
        registry_status,
        "- Invocation does not grant authority; every existing approval and external-action gate remains in force.",
        "",
        "## Matrix",
        "",
        "| Skill | Proposed mode | Authority | Required composition | Optional complements | Rationale |",
        "|---|---|---|---|---|---|",
    ]
    for record in data["skills"]:
        authority = record["authority"]
        authority_text = f"{authority['mode']}; source {authority['source_mutation']}; external {authority['external_actions']}"
        required = ", ".join(
            f"{item['skill']} ({item['use']}, {item['proposed_mode']})"
            for item in record["required_composition"]
        ) or "—"
        optional = ", ".join(record["optional_complements"]) or "—"
        lines.append(
            f"| `{record['name']}` | **{record['proposed_mode']}** | {authority_text} | "
            f"{required} | {optional} | {record['rationale']} |"
        )
    lines.extend([
        "",
        "## Composition meanings",
        "",
        "- `handoff`: the upstream read-only stage may invoke the named model-visible downstream stage while preserving the same slug.",
        "- `embedded`: the caller uses the model-visible primitive while retaining artifact ownership.",
        "- `reference`: the caller inherits authoritative instructions or contracts; it does not implicitly invoke the dependency.",
        "- `context`: the caller validates and preserves an upstream decision; it does not delegate its own task.",
        "- Optional complements are discoverable integrations or handoffs, never hidden required cross-package behavior.",
        "",
        "## Approval boundary",
        "",
        "Approval must identify the proposal SHA above. Applying it will be a separate change that updates the canonical registry and generated Claude/Codex metadata together; partial approval is not applied silently.",
        "",
    ])
    return "\n".join(lines)


def _atomic_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--write", action="store_true", help="Write the proposal and review matrix atomically.")
    parser.add_argument("--check", action="store_true", help="Validate committed proposal artifacts (default).")
    args = parser.parse_args(argv)
    if args.write and args.check:
        parser.error("choose --write or --check")
    repo_root = args.repo_root.resolve()
    manifest_path = (args.manifest or repo_root / DEFAULT_MANIFEST).resolve()
    report_path = (args.report or repo_root / DEFAULT_REPORT).resolve()
    try:
        registry = load_registry(repo_root)
        if args.write:
            data = build_manifest(registry)
            _atomic_text(manifest_path, json.dumps(data, indent=2, ensure_ascii=False) + "\n")
            _atomic_text(report_path, render_report(data))
        else:
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
        errors = validate_manifest(registry, data)
        if report_path.read_text(encoding="utf-8") != render_report(data):
            errors.append("invocation proposal: owner-review report drift")
    except (OSError, json.JSONDecodeError, RegistryError, InvocationProposalError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Invocation proposal validation failed: {len(errors)} error(s).", file=sys.stderr)
        return 1
    action = "Wrote and validated" if args.write else "Validated"
    print(f"{action} {len(data['skills'])} invocation recommendations; proposal sha256 {data['proposal_sha256']}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
