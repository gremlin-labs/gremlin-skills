from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

from run_validation import run_commands, write_receipt  # noqa: E402


class ValidationRunnerTests(unittest.TestCase):
    def test_receipt_records_pass_and_failure_without_command_output(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "pass.py").write_text("print('safe')\n", encoding="utf-8")
            (root / "fail.py").write_text("print('sensitive fixture output')\nraise SystemExit(3)\n", encoding="utf-8")
            commands = [
                ("pass", ["python3", "pass.py"]),
                ("fail", ["python3", "fail.py"]),
            ]
            receipt, errors = run_commands(root, commands)
            self.assertEqual("FAILED", receipt["status"])
            self.assertEqual(1, receipt["summary"]["passed"])
            self.assertTrue(errors)
            self.assertNotIn("sensitive fixture output", json.dumps(receipt))
            path = root / "receipt.json"
            write_receipt(path, receipt)
            self.assertEqual(receipt, json.loads(path.read_text(encoding="utf-8")))

    def test_timeout_is_explicit(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            receipt, errors = run_commands(
                Path(temporary),
                [("slow", ["python3", "-c", "import time; time.sleep(2)"])],
                timeout=1,
            )
            self.assertEqual("TIMED_OUT", receipt["checks"][0]["status"])
            self.assertTrue(errors)


if __name__ == "__main__":
    unittest.main()
