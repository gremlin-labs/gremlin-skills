#!/usr/bin/env python3
"""Generate source host metadata and flat Claude/Codex plugin payloads."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any

from package_skills import EXCLUDED_NAMES, EXCLUDED_SUFFIXES, PackagingError, included_files
from skill_registry import RegistryError, SkillRegistry, load_registry


DEFAULT_OUTPUT = Path("dist/plugins")
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
SPECIAL_WORDS = {"seo": "SEO", "turbulencejs": "TurbulenceJS"}


class PluginGenerationError(RuntimeError):
    """Raised when host metadata or a plugin payload cannot be generated safely."""


def package_metadata(repo_root: Path) -> dict[str, Any]:
    path = repo_root / "package.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise PluginGenerationError(f"{path}: {error}") from error
    required = {"name", "version", "description", "license", "author", "repository", "homepage"}
    missing = sorted(required - data.keys())
    if missing:
        raise PluginGenerationError(f"{path}: missing fields: {', '.join(missing)}")
    if data["name"] != "gremlin-skills" or data["license"] != "MIT":
        raise PluginGenerationError(f"{path}: expected gremlin-skills with MIT license")
    if not re.fullmatch(r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?", str(data["version"])):
        raise PluginGenerationError(f"{path}: version must be semantic")
    author = data["author"]
    if not isinstance(author, dict) or author.get("name") != "E.J. Coughlin" or author.get("email") != "ej@gremlinlabs.com":
        raise PluginGenerationError(f"{path}: author must match the approved public identity")
    return data


def _frontmatter_values(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise PluginGenerationError(f"{path}: missing frontmatter")
    values: dict[str, str] = {}
    for raw in match.group(1).splitlines():
        if ":" not in raw:
            continue
        key, value = raw.split(":", 1)
        values[key.strip()] = value.strip().strip('"')
    return values


def display_name(name: str) -> str:
    return " ".join(SPECIAL_WORDS.get(part, part.capitalize()) for part in name.split("-"))


def short_description(description: str) -> str:
    summary = description.split(" Use when", 1)[0].strip().rstrip(".")
    if len(summary) > 64:
        clause = re.split(r"[,;—]", summary, maxsplit=1)[0].strip()
        if len(clause) >= 25:
            summary = clause
    if len(summary) > 64:
        words: list[str] = []
        for word in summary.split():
            candidate = " ".join([*words, word])
            if len(candidate) > 64:
                break
            words.append(word)
        summary = " ".join(words).rstrip(".,;:—-")
    if len(summary) < 25:
        summary = f"{summary} with a guided workflow"
    if not 25 <= len(summary) <= 64:
        raise PluginGenerationError(f"could not derive 25-64 character UI summary from {description!r}")
    return summary


def openai_yaml(record: dict[str, Any], skill_path: Path) -> str:
    values = _frontmatter_values(skill_path / "SKILL.md")
    description = values.get("description", "")
    if not description:
        raise PluginGenerationError(f"{skill_path / 'SKILL.md'}: missing description")
    name = record["name"]
    shown_name = display_name(name)
    summary = short_description(description)
    prompt = f"Use ${name} to apply the {shown_name} workflow to this request."
    implicit = "true" if record["invocation"]["codex"] == "model-visible" else "false"
    return (
        "interface:\n"
        f"  display_name: {json.dumps(shown_name, ensure_ascii=False)}\n"
        f"  short_description: {json.dumps(summary, ensure_ascii=False)}\n"
        f"  default_prompt: {json.dumps(prompt, ensure_ascii=False)}\n"
        "policy:\n"
        f"  allow_implicit_invocation: {implicit}\n"
    )


def check_openai_metadata(registry: SkillRegistry) -> list[str]:
    errors: list[str] = []
    for record in registry.promoted:
        skill_path = registry.skill_path(record)
        path = skill_path / "agents" / "openai.yaml"
        expected = openai_yaml(record, skill_path)
        if not path.is_file():
            errors.append(f"{path}: missing generated Codex metadata")
        elif path.read_text(encoding="utf-8") != expected:
            errors.append(f"{path}: generated Codex metadata drift")
    return errors


def write_openai_metadata(registry: SkillRegistry) -> None:
    for record in registry.promoted:
        skill_path = registry.skill_path(record)
        path = skill_path / "agents" / "openai.yaml"
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_name(f".{path.name}.tmp")
        temporary.write_text(openai_yaml(record, skill_path), encoding="utf-8")
        temporary.replace(path)


def claude_skill_markdown(source: str, mode: str) -> str:
    match = FRONTMATTER_RE.match(source)
    if not match:
        raise PluginGenerationError("Claude staging requires valid SKILL.md frontmatter")
    lines = [line for line in match.group(1).splitlines() if not line.startswith("disable-model-invocation:")]
    if mode == "user-only":
        lines.append("disable-model-invocation: true")
    return "---\n" + "\n".join(lines) + "\n---\n" + source[match.end():]


def plugin_manifest(host: str, package: dict[str, Any]) -> dict[str, Any]:
    repository = "https://github.com/gremlin-labs/gremlin-skills"
    common: dict[str, Any] = {
        "name": "gremlin-skills",
        "version": package["version"],
        "description": package["description"],
        "author": {
            "name": package["author"]["name"],
            "email": package["author"]["email"],
            "url": "https://github.com/gremlin-labs",
        },
        "homepage": package["homepage"],
        "repository": repository,
        "license": package["license"],
        "keywords": ["agent-skills", "codex", "claude-code", "software-development"],
        "skills": "./skills/",
    }
    if host == "claude":
        return {"displayName": "Gremlin Skills", **common}
    if host != "codex":
        raise PluginGenerationError(f"unknown plugin host {host!r}")
    common["interface"] = {
        "displayName": "Gremlin Skills",
        "shortDescription": "A very particular set of software-building skills",
        "longDescription": (
            "Evidence-heavy workflows for planning, audits, design and product direction, growth systems, "
            "and verified software execution."
        ),
        "developerName": "Gremlin Labs",
        "category": "Developer Tools",
        "capabilities": ["Read", "Write"],
        "websiteURL": repository,
        "defaultPrompt": [
            "Plan a software change with Planpro.",
            "Audit a product workflow before implementation.",
            "Drive an approved plan to completion with Goalpro.",
        ],
        "brandColor": "#85FF00",
    }
    return common


def _copy_skill(source: Path, destination: Path, record: dict[str, Any], host: str) -> None:
    destination.mkdir(parents=True, exist_ok=False)
    for path in included_files(source):
        relative = path.relative_to(source)
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        payload = path.read_bytes()
        if host == "claude" and relative == Path("SKILL.md"):
            payload = claude_skill_markdown(payload.decode("utf-8"), record["invocation"]["claude"]).encode("utf-8")
        target.write_bytes(payload)
        target.chmod(0o755 if path.stat().st_mode & 0o111 else 0o644)


def _tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        relative = path.relative_to(root).as_posix().encode("utf-8")
        payload = path.read_bytes()
        digest.update(len(relative).to_bytes(4, "big"))
        digest.update(relative)
        digest.update(len(payload).to_bytes(8, "big"))
        digest.update(payload)
    return digest.hexdigest()


def build_plugins(repo_root: Path, output_root: Path, *, clean: bool = False) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    output_root = output_root.resolve()
    registry = load_registry(repo_root)
    if registry.data["invocation_policy"]["status"] != "approved":
        raise PluginGenerationError("invocation policy must be approved before plugin staging")
    metadata_errors = check_openai_metadata(registry)
    if metadata_errors:
        raise PluginGenerationError("; ".join(metadata_errors))
    package = package_metadata(repo_root)
    if clean and output_root.exists():
        shutil.rmtree(output_root)
    output_root.mkdir(parents=True, exist_ok=True)
    hosts: list[dict[str, Any]] = []
    for host, manifest_dir in (("codex", ".codex-plugin"), ("claude", ".claude-plugin")):
        root = output_root / host / "gremlin-skills"
        if root.exists():
            shutil.rmtree(root)
        (root / manifest_dir).mkdir(parents=True)
        for record in registry.promoted:
            _copy_skill(registry.skill_path(record), root / "skills" / record["name"], record, host)
        manifest_path = root / manifest_dir / "plugin.json"
        manifest_path.write_text(json.dumps(plugin_manifest(host, package), indent=2) + "\n", encoding="utf-8")
        shutil.copy2(repo_root / "LICENSE", root / "LICENSE")
        shutil.copy2(repo_root / "THIRD-PARTY-NOTICES.md", root / "THIRD-PARTY-NOTICES.md")
        hosts.append({
            "host": host,
            "skills": len(registry.promoted),
            "tree_sha256": _tree_digest(root),
        })
    receipt = {
        "schema_version": 1,
        "package": "gremlin-skills",
        "version": package["version"],
        "invocation_proposal_sha256": "8ee99a986e4b38c0c4d59576c0690deba7cb51d02b7e09cfae7666a6bec67220",
        "hosts": hosts,
    }
    (output_root / "manifest.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    return receipt


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path)
    parser.add_argument("--write", action="store_true", help="Write source metadata and staged plugin payloads.")
    parser.add_argument("--check", action="store_true", help="Check source metadata only (default).")
    parser.add_argument("--clean", action="store_true", help="Replace only the selected plugin output root.")
    args = parser.parse_args(argv)
    if args.write and args.check:
        parser.error("choose --write or --check")
    repo_root = args.repo_root.resolve()
    output = (args.output or repo_root / DEFAULT_OUTPUT).resolve()
    try:
        registry = load_registry(repo_root)
        if registry.data["invocation_policy"]["status"] != "approved":
            raise PluginGenerationError("invocation policy must be approved")
        package_metadata(repo_root)
        if args.write:
            write_openai_metadata(registry)
            receipt = build_plugins(repo_root, output, clean=args.clean)
            print(f"Generated {len(registry.promoted)} skill metadata files and {len(receipt['hosts'])} plugin payloads.")
        else:
            errors = check_openai_metadata(registry)
            if errors:
                raise PluginGenerationError("; ".join(errors))
            for host in ("codex", "claude"):
                plugin_manifest(host, package_metadata(repo_root))
            print(f"Validated generated host metadata for {len(registry.promoted)} promoted skills.")
    except (OSError, RegistryError, PackagingError, PluginGenerationError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
