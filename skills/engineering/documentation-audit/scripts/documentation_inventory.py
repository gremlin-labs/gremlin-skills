#!/usr/bin/env python3
"""Create a deterministic, read-only documentation inventory."""

from __future__ import annotations
import argparse, hashlib, json, re
from pathlib import Path

EXTENSIONS = {".md", ".mdx", ".txt", ".adoc", ".rst"}
SKIP = {".git", "node_modules", ".next", "dist", "build", "coverage", ".venv", "vendor"}
LEGACY = {"plans", "goals", "audits", "proposals", "migrations", "releases", "tests", "restructures", "brainstorms", "feature-specs"}
LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")

def inventory(root: Path) -> dict:
    files = []
    legacy = []
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if any(part in SKIP for part in rel.parts):
            continue
        if path.is_dir() and len(rel.parts) == 1 and path.name in LEGACY:
            legacy.append(rel.as_posix())
        if not path.is_file() or (path.suffix.lower() not in EXTENSIONS and path.name.lower() != "readme"):
            continue
        raw = path.read_bytes()
        text = raw.decode("utf-8", errors="replace")
        files.append({"path": rel.as_posix(), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(),
                      "headings": [line.lstrip("# ") for line in text.splitlines() if line.startswith("#")],
                      "links": LINK.findall(text)})
    return {"root": str(root), "files": files, "legacy_generated_roots": legacy}

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    data = json.dumps(inventory(args.root.resolve()), indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True); args.output.write_text(data, encoding="utf-8")
    else: print(data, end="")
    return 0
if __name__ == "__main__": raise SystemExit(main())

