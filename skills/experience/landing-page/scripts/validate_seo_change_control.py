#!/usr/bin/env python3
# GENERATED CONTRACT RESOURCE
# contract: seo-change-control
# source: scripts/validate_seo_change_control.py
# source-sha256: 2d84abf3165dfabd36cb1260f2a3dc4340cbbab9cb519658b120065c205815b9
# DO NOT EDIT: run python3 scripts/materialize_contracts.py --write
"""Validate SEO editorial ledgers, digest-bound approvals, and technical scopes."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


LANGUAGE_CLASSES = {"FACTUAL", "DERIVED", "COMPARATIVE", "PERSUASIVE", "NAVIGATIONAL"}
CHANGE_CLASSES = {
    "TITLE",
    "DESCRIPTION",
    "VISIBLE_COPY",
    "FAQ_VISIBLE",
    "FAQ_SCHEMA",
    "MODULE_VISIBILITY",
    "STRUCTURED_DATA",
    "CTA",
    "INTERNAL_LINK_COPY",
    "INTERNAL_LINK_DESTINATION",
}
DISPOSITIONS = {"RETAIN", "RESTORE", "REWRITE", "REJECT"}
TERM_DISPOSITIONS = {"RETAIN", "RESTORE", "REWRITE", "ACCEPT_WITH_EVIDENCE", "REJECT"}
STRUCTURED_DATA_STATES = {"ELIGIBLE", "INELIGIBLE", "UNKNOWN", "NOT_APPLICABLE"}
TECHNICAL_CLASSES = {
    "CANONICAL",
    "REDIRECT",
    "SITEMAP",
    "ROBOTS",
    "INDEX_DIRECTIVE",
    "ROUTING",
    "PAGINATION",
    "RELATIONSHIP_DATA",
    "GEOGRAPHY_DATA",
    "INTERNAL_LINK_DESTINATION",
}
USER_FACING_CLASSES = sorted(CHANGE_CLASSES)


class ValidationError(ValueError):
    """Raised when an artifact violates the SEO change-control contract."""


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValidationError(f"{path}: {error}") from error
    if not isinstance(value, dict):
        raise ValidationError(f"{path}: root must be an object")
    return value


def require_object(value: Any, label: str, errors: list[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        errors.append(f"{label}: expected object")
        return {}
    return value


def require_list(value: Any, label: str, errors: list[str], *, nonempty: bool = False) -> list[Any]:
    if not isinstance(value, list):
        errors.append(f"{label}: expected array")
        return []
    if nonempty and not value:
        errors.append(f"{label}: must not be empty")
    return value


def require_string(value: Any, label: str, errors: list[str]) -> str:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{label}: expected non-empty string")
        return ""
    return value


def require_enum(value: Any, allowed: set[str], label: str, errors: list[str]) -> str:
    if value not in allowed:
        errors.append(f"{label}: expected one of {', '.join(sorted(allowed))}")
        return ""
    return str(value)


def validate_ledger(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if data.get("schema_version") != 1:
        errors.append("schema_version: expected 1")
    for field in ("slug", "revision", "created_at", "approval_receipt"):
        require_string(data.get(field), field, errors)
    if data.get("approval_requirement") != "EXACT":
        errors.append("approval_requirement: expected EXACT")

    families = require_list(data.get("page_families"), "page_families", errors, nonempty=True)
    family_names: set[str] = set()
    family_by_name: dict[str, dict[str, Any]] = {}
    for index, raw_family in enumerate(families):
        label = f"page_families[{index}]"
        family = require_object(raw_family, label, errors)
        name = require_string(family.get("name"), f"{label}.name", errors)
        if name in family_names:
            errors.append(f"{label}.name: duplicate page family '{name}'")
        family_names.add(name)
        family_by_name[name] = family
        route_count = family.get("route_count")
        if not isinstance(route_count, int) or isinstance(route_count, bool) or route_count < 1:
            errors.append(f"{label}.route_count: expected positive integer")
        if not isinstance(family.get("shared_template"), bool):
            errors.append(f"{label}.shared_template: expected boolean")
        require_string(family.get("baseline"), f"{label}.baseline", errors)
        canary = require_object(family.get("canary"), f"{label}.canary", errors)
        needs_canary = isinstance(route_count, int) and route_count > 1 or family.get("shared_template") is True
        if canary.get("required") is not needs_canary:
            errors.append(f"{label}.canary.required: expected {str(needs_canary).lower()}")
        if needs_canary:
            require_list(canary.get("routes"), f"{label}.canary.routes", errors, nonempty=True)
            require_list(canary.get("success_signals"), f"{label}.canary.success_signals", errors, nonempty=True)
            require_list(canary.get("failure_signals"), f"{label}.canary.failure_signals", errors, nonempty=True)

    changes = require_list(data.get("changes"), "changes", errors, nonempty=True)
    change_ids: set[str] = set()
    for index, raw_change in enumerate(changes):
        label = f"changes[{index}]"
        change = require_object(raw_change, label, errors)
        change_id = require_string(change.get("id"), f"{label}.id", errors)
        if change_id in change_ids:
            errors.append(f"{label}.id: duplicate change id '{change_id}'")
        change_ids.add(change_id)
        family_name = require_string(change.get("page_family"), f"{label}.page_family", errors)
        if family_name not in family_by_name:
            errors.append(f"{label}.page_family: unknown page family '{family_name}'")
        require_string(change.get("representative_route"), f"{label}.representative_route", errors)
        require_enum(change.get("change_class"), CHANGE_CLASSES, f"{label}.change_class", errors)
        require_enum(change.get("language_class"), LANGUAGE_CLASSES, f"{label}.language_class", errors)
        for field in (
            "before",
            "proposed_after",
            "transformation_rule",
            "intent_effect",
            "ctr_mechanism",
            "persuasion_effect",
            "conversion_mechanism",
            "visible_content_value",
            "baseline",
            "canary_boundary",
            "rollout_boundary",
            "rollback_boundary",
            "specialist_owner",
        ):
            require_string(change.get(field), f"{label}.{field}", errors)
        require_list(change.get("relevant_queries"), f"{label}.relevant_queries", errors, nonempty=True)
        require_list(change.get("terms_gained"), f"{label}.terms_gained", errors)
        terms_lost = require_list(change.get("terms_lost"), f"{label}.terms_lost", errors)
        lost_dispositions = require_object(
            change.get("lost_term_dispositions"), f"{label}.lost_term_dispositions", errors
        )
        for term in terms_lost:
            if not isinstance(term, str) or not term.strip():
                errors.append(f"{label}.terms_lost: every term must be a non-empty string")
                continue
            require_enum(
                lost_dispositions.get(term),
                TERM_DISPOSITIONS,
                f"{label}.lost_term_dispositions[{term!r}]",
                errors,
            )
        extra_term_dispositions = sorted(set(lost_dispositions) - {term for term in terms_lost if isinstance(term, str)})
        if extra_term_dispositions:
            errors.append(f"{label}.lost_term_dispositions: entries without lost terms: {', '.join(extra_term_dispositions)}")
        support = require_object(change.get("support"), f"{label}.support", errors)
        require_list(support.get("sources"), f"{label}.support.sources", errors)
        require_list(
            support.get("available_unused_evidence"),
            f"{label}.support.available_unused_evidence",
            errors,
        )
        require_enum(
            change.get("structured_data_eligibility"),
            STRUCTURED_DATA_STATES,
            f"{label}.structured_data_eligibility",
            errors,
        )
        if not isinstance(change.get("protected_winner"), bool):
            errors.append(f"{label}.protected_winner: expected boolean")
        require_enum(change.get("disposition"), DISPOSITIONS, f"{label}.disposition", errors)
        if change.get("approval_requirement") != "EXACT":
            errors.append(f"{label}.approval_requirement: expected EXACT")

        improve = require_object(change.get("improve_before_remove"), f"{label}.improve_before_remove", errors)
        require_list(improve.get("evidence_reviewed"), f"{label}.improve_before_remove.evidence_reviewed", errors)
        require_string(improve.get("improvement_attempt"), f"{label}.improve_before_remove.improvement_attempt", errors)
        require_enum(
            improve.get("decision"),
            {"IMPROVE", "REMOVE", "RETAIN", "BLOCKED", "NOT_APPLICABLE"},
            f"{label}.improve_before_remove.decision",
            errors,
        )
        if improve.get("decision") == "REMOVE" and not support.get("available_unused_evidence"):
            errors.append(f"{label}: removal requires an explicit available-unused-evidence review")

        rationale_tags = require_list(change.get("rationale_tags"), f"{label}.rationale_tags", errors)
        decision_basis = require_list(change.get("decision_basis"), f"{label}.decision_basis", errors, nonempty=True)
        if change.get("change_class") == "FAQ_VISIBLE" and decision_basis == ["STRUCTURED_DATA_INELIGIBLE"]:
            errors.append(f"{label}: visible FAQ disposition cannot rely only on structured-data ineligibility")
        if "REPEATED_COPY" in rationale_tags:
            duplication = require_object(
                change.get("duplication_assessment"), f"{label}.duplication_assessment", errors
            )
            for field in ("page_level_unique_value", "shared_copy_user_value", "entity_specific_improvement"):
                require_string(duplication.get(field), f"{label}.duplication_assessment.{field}", errors)

    return errors


def validate_approval(data: dict[str, Any], ledger_path: Path, ledger: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if data.get("schema_version") != 1:
        errors.append("approval.schema_version: expected 1")
    expected_digest = hashlib.sha256(ledger_path.read_bytes()).hexdigest()
    if data.get("ledger_sha256") != expected_digest:
        errors.append("approval.ledger_sha256: does not match exact ledger bytes")
    if data.get("status") != "APPROVED":
        errors.append("approval.status: expected APPROVED")
    for field in ("approval_statement", "approved_by", "approved_at"):
        require_string(data.get(field), f"approval.{field}", errors)
    approved = require_list(data.get("approved_change_ids"), "approval.approved_change_ids", errors, nonempty=True)
    if len(approved) != len(set(item for item in approved if isinstance(item, str))):
        errors.append("approval.approved_change_ids: duplicate id")
    known = {item.get("id") for item in ledger.get("changes", []) if isinstance(item, dict)}
    unknown = sorted(item for item in approved if item not in known)
    if unknown:
        errors.append(f"approval.approved_change_ids: unknown ids: {', '.join(unknown)}")
    require_list(data.get("explicit_exclusions"), "approval.explicit_exclusions", errors)
    return errors


def validate_technical_scope(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if data.get("schema_version") != 1:
        errors.append("schema_version: expected 1")
    for field in ("slug", "strategy_revision", "rollout_boundary", "rollback_boundary"):
        require_string(data.get(field), field, errors)
    require_list(data.get("portfolio_item_ids"), "portfolio_item_ids", errors, nonempty=True)
    allowed = require_list(data.get("allowed_change_classes"), "allowed_change_classes", errors, nonempty=True)
    invalid_allowed = sorted(set(allowed) - TECHNICAL_CLASSES)
    if invalid_allowed:
        errors.append(f"allowed_change_classes: non-technical classes: {', '.join(invalid_allowed)}")
    require_list(data.get("allowed_targets"), "allowed_targets", errors, nonempty=True)
    if data.get("user_facing_changes") != "FORBIDDEN":
        errors.append("user_facing_changes: expected FORBIDDEN")
    editorial_ids = require_list(data.get("editorial_change_ids"), "editorial_change_ids", errors)
    if editorial_ids:
        errors.append("editorial_change_ids: technical scope must be empty")
    prohibited = require_list(
        data.get("prohibited_change_classes"), "prohibited_change_classes", errors, nonempty=True
    )
    missing_prohibited = sorted(set(USER_FACING_CLASSES) - set(prohibited))
    if missing_prohibited:
        errors.append(f"prohibited_change_classes: missing {', '.join(missing_prohibited)}")
    approval = require_object(data.get("approval"), "approval", errors)
    if approval.get("status") != "APPROVED":
        errors.append("approval.status: expected APPROVED")
    for field in ("statement", "approved_by", "approved_at", "approved_artifact"):
        require_string(approval.get(field), f"approval.{field}", errors)
    require_list(data.get("gates"), "gates", errors, nonempty=True)
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", type=Path)
    parser.add_argument("--approval", type=Path)
    parser.add_argument("--technical-scope", type=Path)
    args = parser.parse_args(argv)
    if bool(args.ledger) == bool(args.technical_scope):
        parser.error("choose exactly one of --ledger or --technical-scope")
    if args.approval and not args.ledger:
        parser.error("--approval requires --ledger")

    try:
        if args.ledger:
            ledger = load_json(args.ledger)
            errors = validate_ledger(ledger)
            if args.approval:
                approval = load_json(args.approval)
                errors.extend(validate_approval(approval, args.ledger, ledger))
            summary = f"Validated SEO change ledger with {len(ledger.get('changes', []))} change(s)."
        else:
            scope = load_json(args.technical_scope)
            errors = validate_technical_scope(scope)
            summary = f"Validated technical SEO scope with {len(scope.get('allowed_change_classes', []))} class(es)."
    except ValidationError as error:
        errors = [str(error)]
        summary = ""

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"SEO change-control validation failed: {len(errors)} error(s).", file=sys.stderr)
        return 1
    print(summary)
    print("Schema validity is conformance evidence only; it does not prove SEO improvement.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
