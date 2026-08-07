#!/usr/bin/env python3
"""Validate deterministic schemas for Gremlin skill evaluation fixtures."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from skill_registry import RegistryError, load_registry


def _load(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def validate_trigger_data(data: Any, known_skills: set[str]) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict) or not isinstance(data.get("cases"), list):
        return ["trigger-cases.json: expected an object with a cases array"]
    seen: set[str] = set()
    positives: Counter[str] = Counter()
    near_misses: Counter[str] = Counter()
    for index, case in enumerate(data["cases"]):
        location = f"trigger-cases.json:cases[{index}]"
        if not isinstance(case, dict):
            errors.append(f"{location}: expected an object")
            continue
        for field in ("id", "category", "prompt", "expected_skill", "must_not_win", "rationale"):
            if field not in case:
                errors.append(f"{location}: missing field '{field}'")
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id:
            errors.append(f"{location}: id must be a non-empty string")
        elif case_id in seen:
            errors.append(f"{location}: duplicate id '{case_id}'")
        else:
            seen.add(case_id)
        category = case.get("category")
        if category not in {"positive", "near-miss"}:
            errors.append(f"{location}: category must be 'positive' or 'near-miss'")
        expected = case.get("expected_skill")
        if expected not in known_skills and not (category == "near-miss" and expected == "none"):
            errors.append(f"{location}: unknown expected_skill '{expected}'")
        losers = case.get("must_not_win")
        if not isinstance(losers, list) or not losers:
            errors.append(f"{location}: must_not_win must be a non-empty array")
            losers = []
        for loser in losers:
            if loser not in known_skills:
                errors.append(f"{location}: unknown must_not_win skill '{loser}'")
        if category == "positive" and expected in known_skills:
            positives[expected] += 1
        if category == "near-miss":
            for loser in losers:
                near_misses[loser] += 1
        for field in ("prompt", "rationale"):
            if not isinstance(case.get(field), str) or not case[field].strip():
                errors.append(f"{location}: {field} must be a non-empty string")
    for skill in sorted(known_skills):
        if positives[skill] < 3:
            errors.append(f"trigger-cases.json: skill '{skill}' needs at least 3 positive cases")
        if near_misses[skill] < 2:
            errors.append(f"trigger-cases.json: skill '{skill}' needs at least 2 near-miss cases")
    return errors


def validate_contract_data(data: Any, known_skills: set[str]) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict) or not isinstance(data.get("contracts"), list):
        return ["artifact-contracts.json: expected an object with a contracts array"]
    seen: set[str] = set()
    for index, contract in enumerate(data["contracts"]):
        location = f"artifact-contracts.json:contracts[{index}]"
        if not isinstance(contract, dict):
            errors.append(f"{location}: expected an object")
            continue
        skill = contract.get("skill")
        if skill not in known_skills:
            errors.append(f"{location}: unknown skill '{skill}'")
        elif skill in seen:
            errors.append(f"{location}: duplicate contract for '{skill}'")
        else:
            seen.add(skill)
        if not isinstance(contract.get("output_root"), str) or not contract["output_root"]:
            errors.append(f"{location}: output_root must be a non-empty string")
        files = contract.get("files")
        if not isinstance(files, list) or not files:
            errors.append(f"{location}: files must be a non-empty array")
            continue
        paths: set[str] = set()
        for file_index, file_contract in enumerate(files):
            file_location = f"{location}.files[{file_index}]"
            if not isinstance(file_contract, dict):
                errors.append(f"{file_location}: expected an object")
                continue
            path = file_contract.get("path")
            if not isinstance(path, str) or not path:
                errors.append(f"{file_location}: path must be a non-empty string")
            elif path in paths:
                errors.append(f"{file_location}: duplicate path '{path}'")
            else:
                paths.add(path)
            required = file_contract.get("required")
            if not isinstance(required, bool):
                errors.append(f"{file_location}: required must be boolean")
            if required is False and not isinstance(file_contract.get("condition"), str):
                errors.append(f"{file_location}: conditional files need a condition")
            headings = file_contract.get("headings")
            if not isinstance(headings, list) or not headings or not all(isinstance(item, str) and item for item in headings):
                errors.append(f"{file_location}: headings must be a non-empty string array")
    for skill in sorted(known_skills - seen):
        errors.append(f"artifact-contracts.json: missing contract for '{skill}'")
    return errors


def validate_authority_data(data: Any, records: tuple[dict[str, Any], ...] | list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict) or not isinstance(data.get("cases"), list):
        return ["authority-cases.json: expected an object with a cases array"]
    by_name = {record["name"]: record for record in records}
    seen_ids: set[str] = set()
    seen_skills: set[str] = set()
    fields = {
        "id",
        "skill",
        "prompt",
        "expected_authority",
        "allowed_actions",
        "prohibited_actions",
        "required_gates",
        "failure_if",
    }
    for index, case in enumerate(data["cases"]):
        location = f"authority-cases.json:cases[{index}]"
        if not isinstance(case, dict) or set(case) != fields:
            errors.append(f"{location}: fields do not match schema")
            continue
        case_id = case["id"]
        if not isinstance(case_id, str) or not case_id:
            errors.append(f"{location}: id must be a non-empty string")
        elif case_id in seen_ids:
            errors.append(f"{location}: duplicate id '{case_id}'")
        else:
            seen_ids.add(case_id)
        skill = case["skill"]
        record = by_name.get(skill)
        if record is None:
            errors.append(f"{location}: unknown skill '{skill}'")
        elif skill in seen_skills:
            errors.append(f"{location}: duplicate authority case for '{skill}'")
        else:
            seen_skills.add(skill)
            if case["expected_authority"] != record["authority"]:
                errors.append(f"{location}: expected_authority disagrees with registry")
        if not isinstance(case["prompt"], str) or not case["prompt"].strip():
            errors.append(f"{location}: prompt must be a non-empty string")
        arrays: dict[str, list[str]] = {}
        for field in ("allowed_actions", "prohibited_actions", "required_gates", "failure_if"):
            value = case[field]
            if not isinstance(value, list) or not value or not all(isinstance(item, str) and item for item in value):
                errors.append(f"{location}: {field} must be a non-empty string array")
                arrays[field] = []
            else:
                arrays[field] = value
        overlap = set(arrays.get("allowed_actions", [])) & set(arrays.get("prohibited_actions", []))
        if overlap:
            errors.append(f"{location}: actions cannot be both allowed and prohibited")
    for skill in sorted(by_name.keys() - seen_skills):
        errors.append(f"authority-cases.json: missing authority case for '{skill}'")
    return errors


def validate_quality_data(data: Any, known_skills: set[str]) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict) or not isinstance(data.get("cases"), list):
        return ["quality-cases.json: expected an object with a cases array"]
    seen: set[str] = set()
    for index, case in enumerate(data["cases"]):
        location = f"quality-cases.json:cases[{index}]"
        if not isinstance(case, dict):
            errors.append(f"{location}: expected an object")
            continue
        for field in ("id", "skill", "prompt", "applicable_dimensions", "not_applicable_dimensions", "required_evidence", "failure_if"):
            if field not in case:
                errors.append(f"{location}: missing field '{field}'")
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id:
            errors.append(f"{location}: id must be a non-empty string")
        elif case_id in seen:
            errors.append(f"{location}: duplicate id '{case_id}'")
        else:
            seen.add(case_id)
        if case.get("skill") not in known_skills:
            errors.append(f"{location}: unknown skill '{case.get('skill')}'")
        arrays: dict[str, list[str]] = {}
        for field in ("applicable_dimensions", "not_applicable_dimensions", "required_evidence", "failure_if"):
            value = case.get(field)
            if not isinstance(value, list) or not value or not all(isinstance(item, str) and item for item in value):
                errors.append(f"{location}: {field} must be a non-empty string array")
                arrays[field] = []
            else:
                arrays[field] = value
        overlap = set(arrays.get("applicable_dimensions", [])) & set(arrays.get("not_applicable_dimensions", []))
        if overlap:
            errors.append(f"{location}: dimensions cannot be both applicable and not applicable: {', '.join(sorted(overlap))}")
        if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
            errors.append(f"{location}: prompt must be a non-empty string")
    return errors


def validate_handoff_data(data: Any, known_skills: set[str]) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict) or not isinstance(data.get("cases"), list):
        return ["handoff-cases.json: expected an object with a cases array"]
    seen: set[str] = set()
    valid_states = {"READY", "NEEDS DELTA CONFIRMATION", "BLOCKED", "FULL CRITERIA CONFIRMATION", "RESUME OR RECONCILE"}
    for index, case in enumerate(data["cases"]):
        location = f"handoff-cases.json:cases[{index}]"
        if not isinstance(case, dict):
            errors.append(f"{location}: expected an object")
            continue
        for field in ("id", "producer_skill", "input_kind", "prompt", "approval_status", "expected_state", "expected_action", "failure_if"):
            if field not in case:
                errors.append(f"{location}: missing field '{field}'")
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id:
            errors.append(f"{location}: id must be a non-empty string")
        elif case_id in seen:
            errors.append(f"{location}: duplicate id '{case_id}'")
        else:
            seen.add(case_id)
        if case.get("producer_skill") not in known_skills:
            errors.append(f"{location}: unknown producer_skill '{case.get('producer_skill')}'")
        if case.get("input_kind") not in {"handoff", "raw-goal", "existing-goal"}:
            errors.append(f"{location}: invalid input_kind")
        if case.get("approval_status") not in {"APPROVED", "NOT APPROVED", "PARTIAL", "NOT APPLICABLE"}:
            errors.append(f"{location}: invalid approval_status")
        if case.get("expected_state") not in valid_states:
            errors.append(f"{location}: invalid expected_state")
        for field in ("prompt", "expected_action"):
            if not isinstance(case.get(field), str) or not case[field].strip():
                errors.append(f"{location}: {field} must be a non-empty string")
        failure_if = case.get("failure_if")
        if not isinstance(failure_if, list) or not failure_if or not all(isinstance(item, str) and item for item in failure_if):
            errors.append(f"{location}: failure_if must be a non-empty string array")
    return errors


def validate_product_data(data: Any, known_skills: set[str]) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict) or not isinstance(data.get("cases"), list):
        return ["product-cases.json: expected an object with a cases array"]
    seen: set[str] = set()
    for index, case in enumerate(data["cases"]):
        location = f"product-cases.json:cases[{index}]"
        if not isinstance(case, dict):
            errors.append(f"{location}: expected an object")
            continue
        for field in ("id", "skill", "prompt", "relevant_dimensions", "not_applicable_dimensions", "expected_outputs", "material_question", "failure_if"):
            if field not in case:
                errors.append(f"{location}: missing field '{field}'")
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id:
            errors.append(f"{location}: id must be a non-empty string")
        elif case_id in seen:
            errors.append(f"{location}: duplicate id '{case_id}'")
        else:
            seen.add(case_id)
        if case.get("skill") not in known_skills:
            errors.append(f"{location}: unknown skill '{case.get('skill')}'")
        arrays: dict[str, list[str]] = {}
        for field in ("relevant_dimensions", "not_applicable_dimensions", "expected_outputs", "failure_if"):
            value = case.get(field)
            if not isinstance(value, list) or not value or not all(isinstance(item, str) and item for item in value):
                errors.append(f"{location}: {field} must be a non-empty string array")
                arrays[field] = []
            else:
                arrays[field] = value
        overlap = set(arrays.get("relevant_dimensions", [])) & set(arrays.get("not_applicable_dimensions", []))
        if overlap:
            errors.append(f"{location}: dimensions cannot be both relevant and not applicable: {', '.join(sorted(overlap))}")
        for field in ("prompt", "material_question"):
            if not isinstance(case.get(field), str) or not case[field].strip():
                errors.append(f"{location}: {field} must be a non-empty string")
    return errors


def validate_eval_declarations(
    records: list[dict[str, Any]] | tuple[dict[str, Any], ...],
    triggers: Any,
    contracts: Any,
    quality: Any,
    handoffs: Any,
    products: Any,
) -> list[str]:
    """Ensure registry applicability and committed fixtures agree exactly."""

    actual = {
        "trigger": {
            case.get("expected_skill")
            for case in triggers.get("cases", [])
            if isinstance(case, dict) and case.get("category") == "positive"
        },
        "artifact": {
            contract.get("skill") for contract in contracts.get("contracts", []) if isinstance(contract, dict)
        },
        "quality": {case.get("skill") for case in quality.get("cases", []) if isinstance(case, dict)},
        "handoff": {
            case.get("producer_skill") for case in handoffs.get("cases", []) if isinstance(case, dict)
        },
        "product": {case.get("skill") for case in products.get("cases", []) if isinstance(case, dict)},
    }
    errors: list[str] = []
    for record in records:
        name = record["name"]
        declared = set(record["evals"])
        for family, covered in actual.items():
            if family in declared and name not in covered:
                errors.append(f"registry skill '{name}' declares {family} evals but has no fixture")
            if family not in declared and name in covered:
                errors.append(f"registry skill '{name}' has a {family} fixture but does not declare that family")
    return errors


def validate(
    repo_root: Path,
    trigger_path: Path | None = None,
    contract_path: Path | None = None,
    authority_path: Path | None = None,
    quality_path: Path | None = None,
    handoff_path: Path | None = None,
    product_path: Path | None = None,
) -> tuple[int, int, int, int, int, int, list[str]]:
    try:
        registry = load_registry(repo_root)
    except RegistryError as error:
        return 0, 0, 0, 0, 0, 0, str(error).splitlines()
    known_skills = set(registry.names)
    trigger_path = trigger_path or repo_root / "evals" / "trigger-cases.json"
    contract_path = contract_path or repo_root / "evals" / "artifact-contracts.json"
    authority_path = authority_path or repo_root / "evals" / "authority-cases.json"
    quality_path = quality_path or repo_root / "evals" / "quality-cases.json"
    handoff_path = handoff_path or repo_root / "evals" / "handoff-cases.json"
    product_path = product_path or repo_root / "evals" / "product-cases.json"
    try:
        triggers = _load(trigger_path)
        contracts = _load(contract_path)
        authority = _load(authority_path)
        quality = _load(quality_path)
        handoffs = _load(handoff_path)
        products = _load(product_path)
    except (OSError, json.JSONDecodeError) as error:
        return 0, 0, 0, 0, 0, 0, [str(error)]
    errors = validate_trigger_data(triggers, known_skills)
    errors.extend(validate_contract_data(contracts, known_skills))
    errors.extend(validate_authority_data(authority, registry.records))
    errors.extend(validate_quality_data(quality, known_skills))
    errors.extend(validate_handoff_data(handoffs, known_skills))
    errors.extend(validate_product_data(products, known_skills))
    errors.extend(validate_eval_declarations(registry.records, triggers, contracts, quality, handoffs, products))
    return (
        len(triggers.get("cases", [])),
        len(contracts.get("contracts", [])),
        len(authority.get("cases", [])),
        len(quality.get("cases", [])),
        len(handoffs.get("cases", [])),
        len(products.get("cases", [])),
        errors,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--trigger-cases", type=Path)
    parser.add_argument("--artifact-contracts", type=Path)
    parser.add_argument("--authority-cases", type=Path)
    parser.add_argument("--quality-cases", type=Path)
    parser.add_argument("--handoff-cases", type=Path)
    parser.add_argument("--product-cases", type=Path)
    args = parser.parse_args(argv)
    case_count, contract_count, authority_count, quality_count, handoff_count, product_count, errors = validate(
        args.repo_root.resolve(),
        args.trigger_cases,
        args.artifact_contracts,
        args.authority_cases,
        args.quality_cases,
        args.handoff_cases,
        args.product_cases,
    )
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Evaluation validation failed: {len(errors)} error(s).", file=sys.stderr)
        return 1
    print(
        f"Validated {case_count} trigger cases, {contract_count} artifact contracts, {authority_count} authority cases, "
        f"{quality_count} quality cases, {handoff_count} handoff cases, and {product_count} product cases."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
