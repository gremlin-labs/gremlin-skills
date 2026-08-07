from __future__ import annotations
import json, subprocess, sys, tempfile, unittest
from pathlib import Path
from inventory_history import inventory, tree_digest
from validate_manifest import canonical_digest, validate

class ToolTests(unittest.TestCase):
    def test_inventory_excludes_reserved(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); (root/"slug"/"goalpro").mkdir(parents=True); (root/"slug"/"WORK.md").write_text("x"); (root/"• compact-history").mkdir()
            data=inventory(root); self.assertEqual(["slug"],[x["slug"] for x in data["initiatives"]])
    def test_manifest_digest_and_paths(self):
        data={"schema_version":1,"run_id":"run","agent_work_root":"/tmp/work","operations":[{"id":"1","kind":"move_tree","source":"slug","destination":"• compact-history/archive/slug","source_tree_sha256":"a" * 64}]}
        data["confirmation_sha256"]=canonical_digest(data); self.assertEqual([],validate(data))
        data["operations"][0]["source"]="../escape"; self.assertTrue(validate(data))
    def test_manifest_requires_confirmation_digest(self):
        data={"schema_version":1,"run_id":"run","agent_work_root":"/tmp/work","operations":[]}
        self.assertTrue(any("confirmation_sha256" in error for error in validate(data)))
    def test_tree_digest_changes(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); (root/"a").write_text("one"); first,_=tree_digest(root); (root/"a").write_text("two"); second,_=tree_digest(root); self.assertNotEqual(first,second)
    def test_apply_compaction_moves_only_confirmed_tree(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); source=root/"slug"; source.mkdir(); (source/"WORK.md").write_text("done")
            digest,_=tree_digest(source)
            data={"schema_version":1,"run_id":"run-1","agent_work_root":str(root),"operations":[{"id":"move-1","kind":"move_tree","source":"slug","destination":"• compact-history/archive/slug","source_tree_sha256":digest}]}
            data["confirmation_sha256"]=canonical_digest(data)
            manifest=root/"manifest.json"; manifest.write_text(json.dumps(data))
            script=Path(__file__).with_name("apply_compaction.py")
            rejected=subprocess.run([sys.executable,str(script),str(manifest),"--confirm","run-1","--apply"],capture_output=True,text=True)
            self.assertEqual(2,rejected.returncode)
            self.assertTrue(source.is_dir())
            subprocess.run([sys.executable,str(script),str(manifest),"--confirm",f"sha256:{data['confirmation_sha256']}","--apply"],check=True,capture_output=True,text=True)
            self.assertFalse(source.exists()); self.assertTrue((root/"• compact-history"/"archive"/"slug"/"WORK.md").is_file())
            journal=root/"• compact-history"/"runs"/"run-1"/"recovery-journal.json"
            self.assertEqual("completed",json.loads(journal.read_text())["state"])
            subprocess.run([sys.executable,str(script),str(manifest),"--confirm",f"sha256:{data['confirmation_sha256']}","--rollback"],check=True,capture_output=True,text=True)
            self.assertTrue(source.is_dir()); self.assertFalse((root/"• compact-history"/"archive"/"slug").exists())
            self.assertEqual("rolled-back",json.loads(journal.read_text())["state"])
if __name__ == "__main__": unittest.main()
