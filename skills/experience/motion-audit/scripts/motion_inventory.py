#!/usr/bin/env python3
"""Inventory candidate motion syntax without claiming findings."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


PATTERNS = {
    "css-animation": re.compile(r"(?:animation(?:-[\w-]+)?\s*:|@keyframes\b)"),
    "css-transition": re.compile(r"transition(?:-[\w-]+)?\s*:"),
    "reduced-motion": re.compile(r"prefers-reduced-motion|useReducedMotion\b"),
    "pointer-capability": re.compile(r"\b(?:hover|pointer)\s*:|matchMedia\([^\n]*(?:hover|pointer)"),
    "waapi": re.compile(r"\.animate\s*\("),
    "animation-frame": re.compile(r"requestAnimationFrame\s*\("),
    "motion-library": re.compile(r"\b(?:motion\.|useSpring\b|useMotionValue\b|gsap\.|anime\s*\(|turbulencejs(?:/[\w-]+)?)"),
    "gesture": re.compile(r"\b(?:onPointer(?:Down|Move|Up|Cancel)|setPointerCapture|releasePointerCapture|drag(?:Constraints|Elastic)?\b)"),
}

DEFAULT_EXTENSIONS = {".css", ".scss", ".sass", ".less", ".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte"}
SKIP_DIRS = {".git", "node_modules", ".next", "dist", "build", "coverage", "vendor"}


def inventory(root: Path) -> list[dict[str, object]]:
    matches: list[dict[str, object]] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in DEFAULT_EXTENSIONS:
            continue
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeDecodeError):
            continue
        for number, line in enumerate(lines, start=1):
            kinds = [name for name, pattern in PATTERNS.items() if pattern.search(line)]
            if kinds:
                matches.append({"path": str(path.relative_to(root)), "line": number, "kinds": kinds, "text": line.strip()[:240]})
    return matches


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", type=Path)
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of tab-separated candidates")
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        parser.error(f"not a directory: {root}")
    matches = inventory(root)
    if args.json:
        print(json.dumps({"root": str(root), "candidates": matches}, indent=2))
    else:
        for match in matches:
            print(f"{match['path']}:{match['line']}\t{','.join(match['kinds'])}\t{match['text']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
