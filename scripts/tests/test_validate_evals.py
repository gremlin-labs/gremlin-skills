from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

from validate_evals import (  # noqa: E402
    validate_authority_data,
    validate_contract_data,
    validate_eval_declarations,
    validate_handoff_data,
    validate_product_data,
    validate_quality_data,
    validate_trigger_data,
)


SKILLS = {"alpha", "beta"}


def valid_triggers() -> dict:
    cases = []
    for skill, other in (("alpha", "beta"), ("beta", "alpha")):
        for index in range(3):
            cases.append({
                "id": f"{skill}-positive-{index}",
                "category": "positive",
                "prompt": f"Use {skill} for case {index}",
                "expected_skill": skill,
                "must_not_win": [other],
                "rationale": "Direct trigger.",
            })
        for index in range(2):
            cases.append({
                "id": f"{skill}-near-{index}",
                "category": "near-miss",
                "prompt": f"This resembles {skill} but needs {other}",
                "expected_skill": other,
                "must_not_win": [skill],
                "rationale": "Boundary trigger.",
            })
    return {"version": 1, "cases": cases}


def valid_contracts() -> dict:
    return {
        "version": 1,
        "contracts": [
            {
                "skill": skill,
                "output_root": f"outputs/{skill}/{{slug}}/",
                "files": [
                    {"path": "MAIN.md", "required": True, "headings": ["Goal"]},
                    {"path": "NOTES.md", "required": False, "condition": "Only when notes exist.", "headings": ["Notes"]},
                ],
            }
            for skill in sorted(SKILLS)
        ],
    }


def valid_authority() -> tuple[dict, tuple[dict, ...]]:
    records = tuple({
        "name": skill,
        "authority": {"mode": "read-only", "source_mutation": "never", "external_actions": "none"},
    } for skill in sorted(SKILLS))
    data = {
        "version": 1,
        "cases": [{
            "id": f"{skill}-authority",
            "skill": skill,
            "prompt": f"Use {skill} safely.",
            "expected_authority": copy.deepcopy(record["authority"]),
            "allowed_actions": ["Inspect evidence."],
            "prohibited_actions": ["Edit source."],
            "required_gates": ["Remain read-only."],
            "failure_if": ["Source is edited."],
        } for skill, record in ((record["name"], record) for record in records)],
    }
    return data, records


def valid_quality() -> dict:
    return {
        "version": 1,
        "cases": [{
            "id": "quality-alpha",
            "skill": "alpha",
            "prompt": "Implement a user-visible change.",
            "applicable_dimensions": ["Product intent", "Accessibility"],
            "not_applicable_dimensions": ["Data migration"],
            "required_evidence": ["A user-journey test"],
            "failure_if": ["Accessibility is silently omitted"],
        }],
    }


def valid_handoffs() -> dict:
    return {
        "version": 1,
        "cases": [{
            "id": "handoff-ready",
            "producer_skill": "alpha",
            "input_kind": "handoff",
            "prompt": "Execute the approved handoff.",
            "approval_status": "APPROVED",
            "expected_state": "READY",
            "expected_action": "Begin without repeating unchanged approval.",
            "failure_if": ["The full criteria are re-confirmed"],
        }],
    }


def valid_products() -> dict:
    return {
        "version": 1,
        "cases": [{
            "id": "product-alpha",
            "skill": "alpha",
            "prompt": "Plan a user-visible change.",
            "relevant_dimensions": ["User and problem", "Desired outcome"],
            "not_applicable_dimensions": ["Data migration"],
            "expected_outputs": ["A cited user journey"],
            "material_question": "Which recovery behavior should users receive?",
            "failure_if": ["The plan invents a metric"],
        }],
    }


class EvaluationValidatorTests(unittest.TestCase):
    def assert_has_error(self, errors: list[str], phrase: str) -> None:
        self.assertTrue(any(phrase in error for error in errors), errors)

    def test_valid_data(self) -> None:
        self.assertEqual([], validate_trigger_data(valid_triggers(), SKILLS))
        self.assertEqual([], validate_contract_data(valid_contracts(), SKILLS))
        authority, records = valid_authority()
        self.assertEqual([], validate_authority_data(authority, records))
        self.assertEqual([], validate_quality_data(valid_quality(), SKILLS))
        self.assertEqual([], validate_handoff_data(valid_handoffs(), SKILLS))
        self.assertEqual([], validate_product_data(valid_products(), SKILLS))

    def test_duplicate_trigger_id(self) -> None:
        data = valid_triggers()
        data["cases"][1]["id"] = data["cases"][0]["id"]
        self.assert_has_error(validate_trigger_data(data, SKILLS), "duplicate id")

    def test_unknown_skill(self) -> None:
        data = valid_triggers()
        data["cases"][0]["expected_skill"] = "unknown"
        self.assert_has_error(validate_trigger_data(data, SKILLS), "unknown expected_skill")

    def test_near_miss_can_truthfully_have_no_skill_owner(self) -> None:
        data = valid_triggers()
        near_miss = next(case for case in data["cases"] if case["category"] == "near-miss")
        near_miss["expected_skill"] = "none"
        self.assertEqual([], validate_trigger_data(data, SKILLS))

    def test_minimum_case_counts(self) -> None:
        data = valid_triggers()
        data["cases"] = [case for case in data["cases"] if case["id"] != "alpha-positive-2"]
        self.assert_has_error(validate_trigger_data(data, SKILLS), "at least 3 positive")

    def test_missing_contract_and_duplicate_contract(self) -> None:
        data = valid_contracts()
        data["contracts"] = [data["contracts"][0], copy.deepcopy(data["contracts"][0])]
        errors = validate_contract_data(data, SKILLS)
        self.assert_has_error(errors, "duplicate contract")
        self.assert_has_error(errors, "missing contract")

    def test_conditional_file_needs_condition(self) -> None:
        data = valid_contracts()
        del data["contracts"][0]["files"][1]["condition"]
        self.assert_has_error(validate_contract_data(data, SKILLS), "need a condition")

    def test_quality_dimensions_cannot_overlap(self) -> None:
        data = valid_quality()
        data["cases"][0]["not_applicable_dimensions"].append("Accessibility")
        self.assert_has_error(validate_quality_data(data, SKILLS), "both applicable and not applicable")

    def test_authority_must_match_registry_and_cover_every_skill(self) -> None:
        data, records = valid_authority()
        data["cases"][0]["expected_authority"]["source_mutation"] = "task-scoped"
        data["cases"].pop()
        errors = validate_authority_data(data, records)
        self.assert_has_error(errors, "disagrees with registry")
        self.assert_has_error(errors, "missing authority case")

    def test_quality_unknown_skill(self) -> None:
        data = valid_quality()
        data["cases"][0]["skill"] = "unknown"
        self.assert_has_error(validate_quality_data(data, SKILLS), "unknown skill")

    def test_handoff_invalid_state(self) -> None:
        data = valid_handoffs()
        data["cases"][0]["expected_state"] = "MAYBE"
        self.assert_has_error(validate_handoff_data(data, SKILLS), "invalid expected_state")

    def test_handoff_duplicate_id(self) -> None:
        data = valid_handoffs()
        data["cases"].append(copy.deepcopy(data["cases"][0]))
        self.assert_has_error(validate_handoff_data(data, SKILLS), "duplicate id")

    def test_product_dimensions_cannot_overlap(self) -> None:
        data = valid_products()
        data["cases"][0]["not_applicable_dimensions"].append("Desired outcome")
        self.assert_has_error(validate_product_data(data, SKILLS), "both relevant and not applicable")

    def test_product_unknown_skill(self) -> None:
        data = valid_products()
        data["cases"][0]["skill"] = "unknown"
        self.assert_has_error(validate_product_data(data, SKILLS), "unknown skill")

    def test_registry_declared_family_requires_fixture(self) -> None:
        records = (
            {"name": "alpha", "evals": ["trigger", "artifact", "quality"]},
            {"name": "beta", "evals": ["trigger", "artifact"]},
        )
        errors = validate_eval_declarations(
            records,
            valid_triggers(),
            valid_contracts(),
            {"version": 1, "cases": []},
            {"version": 1, "cases": []},
            {"version": 1, "cases": []},
        )
        self.assert_has_error(errors, "alpha' declares quality evals but has no fixture")

    def test_fixture_for_undeclared_family_fails(self) -> None:
        records = (
            {"name": "alpha", "evals": ["trigger", "artifact"]},
            {"name": "beta", "evals": ["trigger", "artifact"]},
        )
        errors = validate_eval_declarations(
            records,
            valid_triggers(),
            valid_contracts(),
            valid_quality(),
            {"version": 1, "cases": []},
            {"version": 1, "cases": []},
        )
        self.assert_has_error(errors, "alpha' has a quality fixture but does not declare")


if __name__ == "__main__":
    unittest.main()
