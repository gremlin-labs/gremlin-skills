from __future__ import annotations

import sys
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

from execute_forward_evals import classify, routing_prompt  # noqa: E402


class ExecuteForwardEvaluationTests(unittest.TestCase):
    def job(self, *, mode: str = "implicit") -> dict:
        return {
            "prompt": "Write a phased plan for this feature.",
            "invocation": {"mode": mode, "skill": "planpro" if mode == "explicit" else None},
            "expected": {"winner": "planpro", "must_not_win": ["goalpro"]},
        }

    def test_prompt_does_not_expose_hidden_expectation(self) -> None:
        prompt = routing_prompt(self.job())
        self.assertIn("Write a phased plan", prompt)
        self.assertIn("null when no installed skill owns it", prompt)
        self.assertNotIn("planpro", prompt)
        self.assertNotIn("goalpro", prompt)

    def test_explicit_prompt_uses_host_native_skill_token(self) -> None:
        prompt = routing_prompt(self.job(mode="explicit"))
        self.assertIn("$planpro", prompt)

    def test_classification_requires_exact_winner_and_boundary(self) -> None:
        self.assertEqual("PASS", classify(self.job(), "planpro"))
        self.assertEqual("FAIL", classify(self.job(), "goalpro"))
        self.assertEqual("FAIL", classify(self.job(), "other"))


if __name__ == "__main__":
    unittest.main()
