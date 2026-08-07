from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1]
ROOT = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))

from skill_registry import load_registry, validate_registry_data  # noqa: E402


class SkillRegistryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.data = json.loads((ROOT / "skills" / "registry.json").read_text(encoding="utf-8"))

    def assert_has_error(self, errors: list[str], phrase: str) -> None:
        self.assertTrue(any(phrase in error for error in errors), errors)

    def test_repository_registry_loads_in_sorted_order(self) -> None:
        registry = load_registry(ROOT)
        self.assertEqual(36, len(registry.records))
        self.assertEqual(tuple(sorted(registry.names)), registry.names)
        self.assertEqual("audit-compare", registry.identities()["audit-compare"])

    def test_duplicate_alias_is_rejected(self) -> None:
        data = copy.deepcopy(self.data)
        data["skills"][1]["aliases"] = [data["skills"][0]["name"]]
        self.assert_has_error(validate_registry_data(data, ROOT, require_paths=False), "already belongs")

    def test_path_escape_is_rejected(self) -> None:
        data = copy.deepcopy(self.data)
        data["skills"][0]["path"] = "skills/../outside"
        self.assert_has_error(validate_registry_data(data, ROOT, require_paths=False), "inside skills")

    def test_records_must_be_deterministic(self) -> None:
        data = copy.deepcopy(self.data)
        data["skills"][0], data["skills"][1] = data["skills"][1], data["skills"][0]
        self.assert_has_error(validate_registry_data(data, ROOT, require_paths=False), "deterministic sorted order")

    def test_unknown_dependency_is_rejected(self) -> None:
        data = copy.deepcopy(self.data)
        data["skills"][0]["dependencies"]["required_skills"] = ["missing-skill"]
        self.assert_has_error(validate_registry_data(data, ROOT, require_paths=False), "unknown skill 'missing-skill'")

    def test_approved_invocation_must_match_both_hosts(self) -> None:
        data = copy.deepcopy(self.data)
        invocation = data["skills"][0]["invocation"]
        invocation.update({"mode": "user-only", "claude": "user-only", "codex": "model-visible"})
        self.assert_has_error(validate_registry_data(data, ROOT, require_paths=False), "Claude and Codex must match")

    def test_published_human_doc_must_exist(self) -> None:
        data = copy.deepcopy(self.data)
        data["skills"][0]["public_docs"] = {
            "path": "docs/skills/definitely-missing.md",
            "status": "published",
        }
        self.assert_has_error(validate_registry_data(data, ROOT), "published document is missing")


if __name__ == "__main__":
    unittest.main()
