from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

from validate_seo_change_control import (  # noqa: E402
    USER_FACING_CLASSES,
    validate_approval,
    validate_ledger,
    validate_technical_scope,
)


class SeoChangeControlTests(unittest.TestCase):
    def valid_ledger(self) -> dict[str, object]:
        return {
            "schema_version": 1,
            "slug": "entity-template-refresh",
            "revision": "r1",
            "created_at": "2026-08-11T12:00:00Z",
            "approval_receipt": "SEO-CHANGE-APPROVAL.json",
            "approval_requirement": "EXACT",
            "page_families": [
                {
                    "name": "where-to-see",
                    "route_count": 419,
                    "shared_template": True,
                    "baseline": "Matched GSC query/page baseline dated 2026-08-10",
                    "canary": {
                        "required": True,
                        "routes": ["/where-to-see/capybara"],
                        "success_signals": ["approved terms and intent remain visible"],
                        "failure_signals": ["copy becomes vaguer or loses approved venue terms"],
                    },
                }
            ],
            "changes": [
                {
                    "id": "wts-description-venue-language",
                    "page_family": "where-to-see",
                    "representative_route": "/where-to-see/capybara",
                    "change_class": "DESCRIPTION",
                    "language_class": "NAVIGATIONAL",
                    "before": "Find zoos, aquariums and wildlife parks where you can see capybaras.",
                    "proposed_after": "Find zoos, aquariums and wildlife parks with capybaras near you.",
                    "transformation_rule": "Preserve supported venue taxonomy and substitute the entity name.",
                    "relevant_queries": ["where to see capybaras", "capybara zoo"],
                    "terms_gained": ["near you"],
                    "terms_lost": [],
                    "lost_term_dispositions": {},
                    "intent_effect": "Preserves venue discovery intent.",
                    "ctr_mechanism": "Keeps specific venue categories visible in the snippet.",
                    "persuasion_effect": "Offers a concrete discovery promise.",
                    "conversion_mechanism": "Moves qualified visitors toward venue detail pages.",
                    "support": {
                        "sources": ["venue taxonomy and entity relationships"],
                        "available_unused_evidence": ["entity traits and venue types"],
                    },
                    "visible_content_value": "Names the destination categories users seek.",
                    "structured_data_eligibility": "NOT_APPLICABLE",
                    "protected_winner": True,
                    "baseline": "Current title/description and matched query performance.",
                    "disposition": "REWRITE",
                    "canary_boundary": "One representative route before template expansion.",
                    "rollout_boundary": "One page family after canary approval.",
                    "rollback_boundary": "Restore the prior description helper independently.",
                    "specialist_owner": "seo-content",
                    "approval_requirement": "EXACT",
                    "improve_before_remove": {
                        "evidence_reviewed": ["facts", "traits", "taxonomy"],
                        "improvement_attempt": "Strengthen the supported venue wording instead of neutralizing it.",
                        "decision": "IMPROVE",
                    },
                    "rationale_tags": [],
                    "decision_basis": ["SEARCH_INTENT", "TAXONOMY", "PERSUASION"],
                }
            ],
        }

    def valid_technical_scope(self) -> dict[str, object]:
        return {
            "schema_version": 1,
            "slug": "entity-template-refresh",
            "strategy_revision": "r3",
            "portfolio_item_ids": ["TECH-12"],
            "allowed_change_classes": ["CANONICAL", "PAGINATION"],
            "allowed_targets": ["src/routes", "src/seo/canonical.ts"],
            "user_facing_changes": "FORBIDDEN",
            "editorial_change_ids": [],
            "prohibited_change_classes": USER_FACING_CLASSES,
            "approval": {
                "status": "APPROVED",
                "statement": "Approved the exact technical targets and classes.",
                "approved_by": "owner",
                "approved_at": "2026-08-11T12:00:00Z",
                "approved_artifact": "agent-work/entity-template-refresh/seo-strategy/GOALPRO-INPUT.md",
            },
            "gates": ["render representative canonical and pagination routes"],
            "rollout_boundary": "One route family after representative verification.",
            "rollback_boundary": "Revert the routing slice without touching content.",
        }

    def test_valid_ledger_passes(self) -> None:
        self.assertEqual([], validate_ledger(self.valid_ledger()))

    def test_lost_terms_require_explicit_dispositions(self) -> None:
        ledger = self.valid_ledger()
        change = ledger["changes"][0]  # type: ignore[index]
        change["terms_lost"] = ["wildlife parks"]  # type: ignore[index]
        errors = validate_ledger(ledger)
        self.assertTrue(any("lost_term_dispositions" in error for error in errors), errors)

    def test_shared_template_requires_canary(self) -> None:
        ledger = self.valid_ledger()
        family = ledger["page_families"][0]  # type: ignore[index]
        family["canary"]["required"] = False  # type: ignore[index]
        errors = validate_ledger(ledger)
        self.assertTrue(any("canary.required" in error for error in errors), errors)

    def test_visible_faq_cannot_be_removed_for_schema_ineligibility_alone(self) -> None:
        ledger = self.valid_ledger()
        change = ledger["changes"][0]  # type: ignore[index]
        change["change_class"] = "FAQ_VISIBLE"  # type: ignore[index]
        change["decision_basis"] = ["STRUCTURED_DATA_INELIGIBLE"]  # type: ignore[index]
        errors = validate_ledger(ledger)
        self.assertTrue(any("visible FAQ" in error for error in errors), errors)

    def test_removal_requires_available_evidence_review(self) -> None:
        ledger = self.valid_ledger()
        change = ledger["changes"][0]  # type: ignore[index]
        change["improve_before_remove"]["decision"] = "REMOVE"  # type: ignore[index]
        change["support"]["available_unused_evidence"] = []  # type: ignore[index]
        errors = validate_ledger(ledger)
        self.assertTrue(any("available-unused-evidence" in error for error in errors), errors)

    def test_digest_bound_approval_detects_byte_drift(self) -> None:
        ledger = self.valid_ledger()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "SEO-CHANGE-LEDGER.json"
            path.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
            approval = {
                "schema_version": 1,
                "ledger_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "status": "APPROVED",
                "approved_change_ids": ["wts-description-venue-language"],
                "approval_statement": "Approved this exact before and after.",
                "approved_by": "owner",
                "approved_at": "2026-08-11T12:05:00Z",
                "explicit_exclusions": [],
            }
            self.assertEqual([], validate_approval(approval, path, ledger))
            path.write_text(path.read_text(encoding="utf-8") + " ", encoding="utf-8")
            errors = validate_approval(approval, path, ledger)
            self.assertTrue(any("exact ledger bytes" in error for error in errors), errors)

    def test_valid_technical_scope_passes(self) -> None:
        self.assertEqual([], validate_technical_scope(self.valid_technical_scope()))

    def test_technical_scope_requires_approval_and_rollout(self) -> None:
        scope = self.valid_technical_scope()
        scope.pop("approval")
        scope.pop("rollout_boundary")
        errors = validate_technical_scope(scope)
        self.assertTrue(any("approval" in error for error in errors), errors)
        self.assertTrue(any("rollout_boundary" in error for error in errors), errors)

    def test_technical_scope_rejects_editorial_work(self) -> None:
        scope = self.valid_technical_scope()
        scope["allowed_change_classes"] = ["CANONICAL", "TITLE"]
        scope["editorial_change_ids"] = ["title-1"]
        errors = validate_technical_scope(scope)
        self.assertTrue(any("non-technical classes" in error for error in errors), errors)
        self.assertTrue(any("must be empty" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
