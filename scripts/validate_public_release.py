#!/usr/bin/env python3
"""Audit the prospective public source tree for local residue and obvious secrets."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path


EXCLUDED_ROOTS = {".git", "agent-work", "dist", "references", "research"}
EXCLUDED_FILES = {".trufflehog-exclude-paths.txt"}
IGNORED_DIRECTORY_NAMES = {
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
    ".nox",
    ".tox",
    ".venv",
    "node_modules",
    "venv",
}
REQUIRED_IGNORE_LINES = {
    "/agent-work/",
    "/dist/",
    "/references/",
    "/research/",
    "/node_modules/",
    "__pycache__/",
    "*.bundle",
    ".DS_Store",
    "/.trufflehog-exclude-paths.txt",
}
SENSITIVE_SUFFIXES = {".key", ".p12", ".pem", ".pfx"}
GENERATED_SUFFIXES = {".pyo", ".pyc"}
LOCAL_PATH_PATTERNS = {
    "macOS user path": re.compile(r"(?<![A-Za-z0-9])/(?:Users)/[A-Za-z0-9._-]+(?:/|\b)"),
    "Linux user path": re.compile(r"(?<![A-Za-z0-9])/(?:home)/[A-Za-z0-9._-]+(?:/|\b)"),
    "macOS private temp path": re.compile(r"(?<![A-Za-z0-9])/(?:private/)?var/folders/[A-Za-z0-9._-]+/"),
    "Windows user path": re.compile(r"(?i)(?:[A-Z]:\\Users\\)[^\\\s]+"),
    "local file URL": re.compile(r"(?i)file:///(?:Users|home)/[A-Za-z0-9._-]+(?:/|\b)"),
}
SECRET_PATTERNS = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "AWS access key": re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
    "GitHub token": re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"),
    "GitLab token": re.compile(r"\bglpat-[A-Za-z0-9_-]{20,}\b"),
    "Slack token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"),
    "Stripe secret": re.compile(r"\b(?:sk|rk)_(?:live|test)_[A-Za-z0-9]{12,}\b"),
    "Google API key": re.compile(r"\bAIza[0-9A-Za-z_-]{30,}\b"),
}


class PublicReleaseError(RuntimeError):
    """Raised when the public-tree audit itself cannot run."""


def _sensitive_name(path: Path) -> bool:
    name = path.name
    if path.suffix.lower() in SENSITIVE_SUFFIXES:
        return True
    return name == ".env" or (name.startswith(".env.") and name != ".env.example")


def _generated_name(path: Path) -> bool:
    return path.name == ".DS_Store" or path.suffix.lower() in GENERATED_SUFFIXES


def public_files(repo_root: Path) -> tuple[list[Path], list[str]]:
    """Return deterministic public files and filesystem-shape errors."""

    repo_root = repo_root.resolve()
    files: list[Path] = []
    errors: list[str] = []
    for current, directories, names in os.walk(repo_root):
        current_path = Path(current)
        relative_dir = current_path.relative_to(repo_root)
        if relative_dir.parts and relative_dir.parts[0] in EXCLUDED_ROOTS:
            directories[:] = []
            continue
        directories[:] = sorted(
            name
            for name in directories
            if name not in IGNORED_DIRECTORY_NAMES
            and not (relative_dir == Path(".") and name in EXCLUDED_ROOTS)
        )
        for name in sorted(names):
            path = current_path / name
            relative = path.relative_to(repo_root)
            if relative.as_posix() in EXCLUDED_FILES:
                continue
            if path.is_symlink():
                errors.append(f"{relative.as_posix()}: symbolic links are not allowed in the public source tree")
                continue
            if _generated_name(path):
                continue
            if _sensitive_name(path):
                errors.append(f"{relative.as_posix()}: sensitive or generated filename is not public-release safe")
                continue
            files.append(path)
    return files, errors


def _check_gitignore(repo_root: Path) -> list[str]:
    path = repo_root / ".gitignore"
    if not path.is_file():
        return [".gitignore: missing"]
    lines = {
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }
    return [f".gitignore: missing required public exclusion '{line}'" for line in sorted(REQUIRED_IGNORE_LINES - lines)]


def _scan_text(path: Path, repo_root: Path) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return []
    relative = path.relative_to(repo_root).as_posix()
    errors: list[str] = []
    for label, pattern in LOCAL_PATH_PATTERNS.items():
        for match in pattern.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            errors.append(f"{relative}:{line}: {label} must use a portable placeholder or runtime temp directory")
    for label, pattern in SECRET_PATTERNS.items():
        for match in pattern.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            errors.append(f"{relative}:{line}: possible {label}; remove it and rotate the credential before release")
    return errors


def _check_index(repo_root: Path) -> list[str]:
    completed = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=repo_root,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise PublicReleaseError("git ls-files failed while checking the release index")
    errors: list[str] = []
    for raw in completed.stdout.decode("utf-8").split("\0"):
        if not raw:
            continue
        path = Path(raw)
        if path.as_posix() in EXCLUDED_FILES:
            errors.append(f"git index includes excluded public file: {raw}")
        if path.parts and path.parts[0] in EXCLUDED_ROOTS:
            errors.append(f"git index includes excluded public path: {raw}")
        if _sensitive_name(path) or _generated_name(path) or any(part in IGNORED_DIRECTORY_NAMES for part in path.parts):
            errors.append(f"git index includes generated or sensitive path: {raw}")
    return errors


def validate_public_release(
    repo_root: Path,
    *,
    check_index: bool = False,
    require_license: bool = False,
) -> tuple[int, list[str]]:
    repo_root = repo_root.resolve()
    files, errors = public_files(repo_root)
    errors.extend(_check_gitignore(repo_root))
    for path in files:
        errors.extend(_scan_text(path, repo_root))
    if require_license:
        license_path = repo_root / "LICENSE"
        if not license_path.is_file() or not license_path.read_text(encoding="utf-8").strip():
            errors.append("LICENSE: owner-approved open-source license is missing")
    if check_index:
        errors.extend(_check_index(repo_root))
    return len(files), errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--check-index", action="store_true", help="Reject excluded or generated paths in Git's index.")
    parser.add_argument("--require-license", action="store_true", help="Require a non-empty root LICENSE file.")
    args = parser.parse_args(argv)
    try:
        count, errors = validate_public_release(
            args.repo_root,
            check_index=args.check_index,
            require_license=args.require_license,
        )
    except (OSError, PublicReleaseError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Public-release audit failed: {len(errors)} error(s) across {count} candidate file(s).", file=sys.stderr)
        return 1
    suffixes = []
    if args.check_index:
        suffixes.append("Git index")
    if args.require_license:
        suffixes.append("license")
    scope = f" including {' and '.join(suffixes)}" if suffixes else ""
    print(f"Validated {count} candidate public files{scope}: no local paths, obvious secrets, or unsafe files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
