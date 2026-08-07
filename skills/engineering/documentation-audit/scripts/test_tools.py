from __future__ import annotations
import tempfile, unittest
from pathlib import Path
from documentation_inventory import inventory
from validate_documentation_catalog import validate

class ToolTests(unittest.TestCase):
    def test_inventory_detects_docs_and_legacy_root(self):
        with tempfile.TemporaryDirectory() as value:
            root = Path(value); (root / "plans").mkdir(); (root / "README.md").write_text("# Hi\n", encoding="utf-8")
            data = inventory(root)
            self.assertEqual("README.md", data["files"][0]["path"]); self.assertEqual(["plans"], data["legacy_generated_roots"])
    def test_catalog_rejects_duplicate_and_invalid_state(self):
        rows = [{"path":"a.md","kind":"GUIDE","freshness":"OLD","implementation":"N/A","authority":"CANONICAL","action":"KEEP","confidence":"HIGH","evidence":[]}] * 2
        errors = validate(rows); self.assertTrue(any("invalid freshness" in e for e in errors)); self.assertTrue(any("duplicate" in e for e in errors))
if __name__ == "__main__": unittest.main()
