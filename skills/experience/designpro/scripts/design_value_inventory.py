#!/usr/bin/env python3
"""Inventory candidate design literals without declaring policy violations."""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


DEFAULT_EXTENSIONS = {
    ".css", ".html", ".js", ".jsx", ".mjs", ".mts", ".sass", ".scss",
    ".tsx", ".ts", ".vue", ".svelte",
}
DEFAULT_EXCLUDES = {
    ".git", ".next", ".nuxt", ".output", ".svelte-kit", "build", "coverage",
    "dist", "node_modules", "out", "storybook-static", "vendor",
}


PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("raw-color", re.compile(
        r"(?<![\w-])(?:#[0-9a-fA-F]{3,8}\b|(?:rgb|rgba|hsl|hsla|hwb|lab|lch|oklab|oklch|color)\([^\n;{}]+\))"
    )),
    ("tailwind-arbitrary", re.compile(
        r"(?<![\w-])(?:bg|text|border|ring|outline|shadow|rounded|p[trblxy]?|m[trblxy]?|gap[xy]?|space-[xy]|w|h|min-w|max-w|min-h|max-h|leading|tracking|font|z|duration|ease)-\[[^\]\n]+\]"
    )),
    ("inline-style", re.compile(
        r"\bstyle\s*=\s*(?:\{\{|\{\s*\{|[\"'])"
    )),
    ("hardcoded-radius", re.compile(
        r"\bborder(?:-top-left|-top-right|-bottom-left|-bottom-right)?-radius\s*:\s*(?!var\()[^;\n}]+"
    )),
    ("hardcoded-shadow", re.compile(
        r"\bbox-shadow\s*:\s*(?!var\()[^;\n}]+"
    )),
    ("hardcoded-font", re.compile(
        r"\bfont-(?:family|size|weight)\s*:\s*(?!var\()[^;\n}]+"
    )),
    ("hardcoded-z-index", re.compile(
        r"\bz-index\s*:\s*(?!var\()[+-]?\d+\b"
    )),
)


def _matches(path: Path, patterns: Iterable[str]) -> bool:
    text = path.as_posix()
    return any(fnmatch.fnmatch(text, pattern) or fnmatch.fnmatch(path.name, pattern) for pattern in patterns)


def _source_files(roots: list[Path], extensions: set[str], excludes: set[str]) -> Iterable[tuple[Path, Path]]:
    seen: set[Path] = set()
    for root in roots:
        resolved = root.resolve()
        candidates = [resolved] if resolved.is_file() else resolved.rglob("*") if resolved.is_dir() else []
        for path in candidates:
            if not path.is_file() or path.suffix.lower() not in extensions:
                continue
            if any(part in excludes for part in path.parts):
                continue
            canonical = path.resolve()
            if canonical in seen:
                continue
            seen.add(canonical)
            display = path.relative_to(Path.cwd()) if path.is_relative_to(Path.cwd()) else path
            yield path, display


def inventory(
    roots: list[Path],
    extensions: set[str] | None = None,
    excludes: set[str] | None = None,
    sanctioned_patterns: list[str] | None = None,
) -> dict[str, Any]:
    extensions = extensions or DEFAULT_EXTENSIONS
    excludes = excludes or DEFAULT_EXCLUDES
    sanctioned_patterns = sanctioned_patterns or []
    candidates: list[dict[str, Any]] = []
    files_scanned = 0
    unreadable: list[str] = []
    for path, display in _source_files(roots, extensions, excludes):
        files_scanned += 1
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            unreadable.append(f"{display}: {error}")
            continue
        sanctioned = _matches(display, sanctioned_patterns)
        for line_number, line in enumerate(text.splitlines(), start=1):
            for category, pattern in PATTERNS:
                for match in pattern.finditer(line):
                    candidates.append({
                        "category": category,
                        "path": display.as_posix(),
                        "line": line_number,
                        "column": match.start() + 1,
                        "match": match.group(0),
                        "sanctioned_source": sanctioned,
                    })
    counts = Counter(item["category"] for item in candidates)
    return {
        "version": 1,
        "disclaimer": "Candidate evidence only. Inspect context and repository policy before classifying a finding.",
        "summary": {
            "files_scanned": files_scanned,
            "candidates": len(candidates),
            "unreadable_files": len(unreadable),
            "by_category": dict(sorted(counts.items())),
        },
        "candidates": candidates,
        "unreadable": unreadable,
    }


def markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Design value inventory",
        "",
        f'> {report["disclaimer"]}',
        "",
        "| Category | File | Line | Match | Sanctioned source |",
        "|---|---|---:|---|---|",
    ]
    for item in report["candidates"]:
        match = item["match"].replace("|", "\\|").replace("`", "\\`")
        lines.append(
            f'| {item["category"]} | `{item["path"]}` | {item["line"]} | `{match}` | '
            f'{"yes" if item["sanctioned_source"] else "no"} |'
        )
    summary = report["summary"]
    lines.extend([
        "",
        f'Files scanned: {summary["files_scanned"]}; candidates: {summary["candidates"]}; '
        f'unreadable: {summary["unreadable_files"]}.',
        "",
    ])
    if report["unreadable"]:
        lines.extend(["## Unreadable files", ""] + [f"- {item}" for item in report["unreadable"]] + [""])
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("roots", nargs="+", type=Path, help="source files or directories")
    parser.add_argument("--extension", action="append", help="included extension; repeatable")
    parser.add_argument("--exclude-dir", action="append", default=[], help="excluded directory name; repeatable")
    parser.add_argument("--sanctioned", action="append", default=[], help="glob for token or sanctioned style sources")
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    parser.add_argument("--output", type=Path, help="write output instead of stdout")
    args = parser.parse_args(argv)
    missing = [str(root) for root in args.roots if not root.exists()]
    if missing:
        print(f'design_value_inventory: missing root(s): {", ".join(missing)}', file=sys.stderr)
        return 2
    extensions = None
    if args.extension:
        extensions = {item if item.startswith(".") else f".{item}" for item in args.extension}
    report = inventory(
        args.roots,
        extensions=extensions,
        excludes=DEFAULT_EXCLUDES | set(args.exclude_dir),
        sanctioned_patterns=args.sanctioned,
    )
    rendered = json.dumps(report, indent=2) + "\n" if args.format == "json" else markdown(report)
    try:
        if args.output:
            args.output.write_text(rendered, encoding="utf-8")
        else:
            sys.stdout.write(rendered)
    except OSError as error:
        print(f"design_value_inventory: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
