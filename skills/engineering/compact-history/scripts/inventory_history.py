#!/usr/bin/env python3
"""Create a deterministic read-only inventory of actionable agent-work slugs."""
from __future__ import annotations
import argparse, hashlib, json, unicodedata
from pathlib import Path

RESERVED = "• compact-history"

def tree_digest(root: Path) -> tuple[str, list[dict]]:
    digest = hashlib.sha256(); files = []
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        rel = path.relative_to(root).as_posix(); raw = path.read_bytes()
        digest.update(rel.encode()); digest.update(b"\0"); digest.update(hashlib.sha256(raw).digest())
        files.append({"path": rel, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()})
    return digest.hexdigest(), files

def inventory(root: Path) -> dict:
    initiatives = []
    for path in sorted(p for p in root.iterdir() if p.is_dir()):
        name = unicodedata.normalize("NFC", path.name)
        if name == RESERVED: continue
        value, files = tree_digest(path)
        initiatives.append({"slug": path.name, "tree_sha256": value, "files": files,
                            "stages": sorted(p.name for p in path.iterdir() if p.is_dir())})
    return {"schema_version": 1, "agent_work_root": str(root.resolve()), "initiatives": initiatives}

def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--agent-work-root",type=Path,required=True); p.add_argument("--output",type=Path); a=p.parse_args()
    data=json.dumps(inventory(a.agent_work_root.resolve()),indent=2)+"\n"
    if a.output: a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(data,encoding="utf-8")
    else: print(data,end="")
    return 0
if __name__ == "__main__": raise SystemExit(main())

