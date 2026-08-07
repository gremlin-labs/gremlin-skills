#!/usr/bin/env python3
"""Load and validate the canonical Gremlin skill registry."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Iterable


NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REGISTRY_RELATIVE_PATH = Path("skills/registry.json")
TOP_LEVEL_FIELDS = {"schema_version", "category_model", "invocation_policy", "skills"}
RECORD_FIELDS = {
    "name",
    "aliases",
    "category",
    "maturity",
    "path",
    "public_docs",
    "invocation",
    "authority",
    "output_root",
    "capabilities",
    "contracts",
    "dependencies",
    "evals",
    "tests",
    "distribution",
    "provenance",
    "deprecation",
}
CAPABILITY_FIELDS = {
    "decision_tree",
    "work_artifacts",
    "readme_registration",
    "theme_library_discovery",
    "goalpro_handoff",
    "quality_report",
    "product_research",
}
EVAL_ORDER = ("trigger", "artifact", "quality", "handoff", "product")
MATURITIES = {"promoted", "incubating", "misc", "deprecated"}
INVOCATION_MODES = {"pending-owner-review", "user-only", "model-visible"}
AUTHORITY_MODES = {"read-only", "executor", "hybrid"}
SOURCE_MUTATION_MODES = {"never", "after-approval", "task-scoped"}
EXTERNAL_ACTION_MODES = {"none", "approval-required"}


class RegistryError(ValueError):
    """Raised when the canonical registry is absent or invalid."""


@dataclass(frozen=True)
class SkillRegistry:
    """Validated registry records in deterministic name order."""

    repo_root: Path
    path: Path
    data: dict[str, Any]
    records: tuple[dict[str, Any], ...]

    @property
    def names(self) -> tuple[str, ...]:
        return tuple(record["name"] for record in self.records)

    @property
    def by_name(self) -> dict[str, dict[str, Any]]:
        return {record["name"]: record for record in self.records}

    @property
    def promoted(self) -> tuple[dict[str, Any], ...]:
        return tuple(record for record in self.records if record["maturity"] == "promoted")

    def skill_path(self, record_or_name: dict[str, Any] | str) -> Path:
        record = self.by_name[record_or_name] if isinstance(record_or_name, str) else record_or_name
        return self.repo_root / PurePosixPath(record["path"])

    def identities(self) -> dict[str, str]:
        result: dict[str, str] = {}
        for record in self.records:
            for identity in (record["name"], *record["aliases"]):
                result[identity] = record["name"]
        return result


def _keys(location: str, value: Any, expected: set[str], errors: list[str]) -> bool:
    if not isinstance(value, dict):
        errors.append(f"{location}: expected an object")
        return False
    missing = sorted(expected - value.keys())
    unknown = sorted(value.keys() - expected)
    if missing:
        errors.append(f"{location}: missing field(s): {', '.join(missing)}")
    if unknown:
        errors.append(f"{location}: unknown field(s): {', '.join(unknown)}")
    return not missing and not unknown


def _string_list(
    location: str,
    value: Any,
    errors: list[str],
    *,
    allow_empty: bool = True,
    sorted_values: bool = True,
) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        errors.append(f"{location}: expected a string array")
        return []
    if not allow_empty and not value:
        errors.append(f"{location}: must not be empty")
    if len(value) != len(set(value)):
        errors.append(f"{location}: values must be unique")
    if sorted_values and value != sorted(value):
        errors.append(f"{location}: values must be sorted")
    return value


def _contained_path(repo_root: Path, raw: Any, location: str, errors: list[str], prefix: str) -> Path | None:
    if not isinstance(raw, str) or not raw:
        errors.append(f"{location}: expected a non-empty relative path")
        return None
    pure = PurePosixPath(raw)
    if pure.is_absolute() or ".." in pure.parts or "." in pure.parts or not pure.parts or pure.parts[0] != prefix:
        errors.append(f"{location}: path must stay inside {prefix}/")
        return None
    resolved = (repo_root / pure).resolve()
    expected_root = (repo_root / prefix).resolve()
    if resolved != expected_root and expected_root not in resolved.parents:
        errors.append(f"{location}: resolved path escapes {prefix}/")
        return None
    return resolved


def validate_registry_data(data: Any, repo_root: Path, *, require_paths: bool = True) -> list[str]:
    """Return precise schema, identity, relationship, and path errors."""

    repo_root = repo_root.resolve()
    errors: list[str] = []
    if not _keys("registry", data, TOP_LEVEL_FIELDS, errors):
        return errors
    if data.get("schema_version") != 1:
        errors.append("registry.schema_version: expected 1")

    category_model = data.get("category_model")
    if _keys("registry.category_model", category_model, {"status", "values"}, errors):
        if category_model["status"] not in {"proposed", "approved"}:
            errors.append("registry.category_model.status: expected proposed or approved")
        categories = _string_list("registry.category_model.values", category_model["values"], errors, allow_empty=False)
    else:
        categories = []

    invocation_policy = data.get("invocation_policy")
    if _keys("registry.invocation_policy", invocation_policy, {"status", "allowed_modes"}, errors):
        if invocation_policy["status"] not in {"pending-owner-review", "approved"}:
            errors.append("registry.invocation_policy.status: invalid status")
        allowed_modes = _string_list(
            "registry.invocation_policy.allowed_modes", invocation_policy["allowed_modes"], errors, allow_empty=False
        )
        if set(allowed_modes) != {"model-visible", "user-only"}:
            errors.append("registry.invocation_policy.allowed_modes: expected model-visible and user-only")

    records = data.get("skills")
    if not isinstance(records, list) or not records:
        return errors + ["registry.skills: expected a non-empty array"]

    seen_identities: dict[str, str] = {}
    seen_paths: dict[str, str] = {}
    record_names: list[str] = []
    valid_records: list[dict[str, Any]] = []
    for index, record in enumerate(records):
        location = f"registry.skills[{index}]"
        if not _keys(location, record, RECORD_FIELDS, errors):
            continue
        valid_records.append(record)
        name = record["name"]
        if not isinstance(name, str) or not NAME_RE.fullmatch(name):
            errors.append(f"{location}.name: expected lowercase kebab-case")
            name = f"invalid-{index}"
        record_names.append(name)

        aliases = _string_list(f"{location}.aliases", record["aliases"], errors)
        for identity in (name, *aliases):
            if not NAME_RE.fullmatch(identity):
                errors.append(f"{location}: identity '{identity}' must be lowercase kebab-case")
            owner = seen_identities.get(identity)
            if owner:
                errors.append(f"{location}: identity '{identity}' already belongs to '{owner}'")
            else:
                seen_identities[identity] = name

        if record["category"] not in categories:
            errors.append(f"{location}.category: unknown category '{record['category']}'")
        if record["maturity"] not in MATURITIES:
            errors.append(f"{location}.maturity: invalid maturity '{record['maturity']}'")

        skill_path = _contained_path(repo_root, record["path"], f"{location}.path", errors, "skills")
        if isinstance(record["path"], str):
            owner = seen_paths.get(record["path"])
            if owner:
                errors.append(f"{location}.path: already owned by '{owner}'")
            else:
                seen_paths[record["path"]] = name
        if require_paths and skill_path is not None:
            if not skill_path.is_dir() or not (skill_path / "SKILL.md").is_file():
                errors.append(f"{location}.path: missing skill directory or SKILL.md at {record['path']}")

        docs = record["public_docs"]
        if _keys(f"{location}.public_docs", docs, {"path", "status"}, errors):
            docs_path = _contained_path(repo_root, docs["path"], f"{location}.public_docs.path", errors, "docs")
            if docs["status"] not in {"planned", "published"}:
                errors.append(f"{location}.public_docs.status: expected planned or published")
            if require_paths and docs["status"] == "published" and docs_path is not None and not docs_path.is_file():
                errors.append(f"{location}.public_docs.path: published document is missing")

        invocation = record["invocation"]
        if _keys(f"{location}.invocation", invocation, {"mode", "claude", "codex"}, errors):
            for field in ("mode", "claude", "codex"):
                if invocation[field] not in INVOCATION_MODES:
                    errors.append(f"{location}.invocation.{field}: invalid invocation mode")
            if invocation["mode"] != "pending-owner-review" and {
                invocation["mode"], invocation["claude"], invocation["codex"]
            } != {invocation["mode"]}:
                errors.append(f"{location}.invocation: Claude and Codex must match the approved mode")

        authority = record["authority"]
        if _keys(f"{location}.authority", authority, {"mode", "source_mutation", "external_actions"}, errors):
            if authority["mode"] not in AUTHORITY_MODES:
                errors.append(f"{location}.authority.mode: invalid authority mode")
            if authority["source_mutation"] not in SOURCE_MUTATION_MODES:
                errors.append(f"{location}.authority.source_mutation: invalid source mutation mode")
            if authority["external_actions"] not in EXTERNAL_ACTION_MODES:
                errors.append(f"{location}.authority.external_actions: invalid external-action mode")
            if authority["mode"] == "read-only" and authority["source_mutation"] != "never":
                errors.append(f"{location}.authority: read-only skills must never mutate source")

        if not isinstance(record["output_root"], str) or not record["output_root"] or "<" in record["output_root"]:
            errors.append(f"{location}.output_root: expected a non-empty brace-placeholder path")

        capabilities = record["capabilities"]
        if _keys(f"{location}.capabilities", capabilities, CAPABILITY_FIELDS, errors):
            for field, value in capabilities.items():
                if not isinstance(value, bool):
                    errors.append(f"{location}.capabilities.{field}: expected boolean")

        _string_list(f"{location}.contracts", record["contracts"], errors, allow_empty=False)
        dependencies = record["dependencies"]
        if _keys(f"{location}.dependencies", dependencies, {"required_skills", "optional_skills"}, errors):
            required = _string_list(f"{location}.dependencies.required_skills", dependencies["required_skills"], errors)
            optional = _string_list(f"{location}.dependencies.optional_skills", dependencies["optional_skills"], errors)
            overlap = set(required) & set(optional)
            if overlap:
                errors.append(f"{location}.dependencies: required and optional overlap: {', '.join(sorted(overlap))}")
            if name in required or name in optional:
                errors.append(f"{location}.dependencies: a skill cannot depend on itself")

        evals = _string_list(
            f"{location}.evals", record["evals"], errors, allow_empty=False, sorted_values=False
        )
        if any(family not in EVAL_ORDER for family in evals):
            errors.append(f"{location}.evals: unknown evaluation family")
        if evals != [family for family in EVAL_ORDER if family in evals]:
            errors.append(f"{location}.evals: families must follow canonical order")

        _string_list(f"{location}.tests", record["tests"], errors)
        distribution = record["distribution"]
        if _keys(
            f"{location}.distribution", distribution, {"standalone_archive", "stable_plugin", "public_install"}, errors
        ):
            for field, value in distribution.items():
                if not isinstance(value, bool):
                    errors.append(f"{location}.distribution.{field}: expected boolean")

        provenance = record["provenance"]
        if _keys(f"{location}.provenance", provenance, {"origin", "acknowledgements"}, errors):
            if provenance["origin"] != "gremlin-skills":
                errors.append(f"{location}.provenance.origin: expected gremlin-skills")
            _string_list(f"{location}.provenance.acknowledgements", provenance["acknowledgements"], errors)

        if record["maturity"] != "deprecated" and record["deprecation"] is not None:
            errors.append(f"{location}.deprecation: only deprecated skills may carry migration metadata")

    if record_names != sorted(record_names) or len(record_names) != len(set(record_names)):
        errors.append("registry.skills: records must have unique names in deterministic sorted order")

    known_names = {record["name"] for record in valid_records if isinstance(record.get("name"), str)}
    for index, record in enumerate(valid_records):
        dependencies = record["dependencies"]
        if not isinstance(dependencies, dict):
            continue
        for field in ("required_skills", "optional_skills"):
            values = dependencies.get(field, [])
            if not isinstance(values, list):
                continue
            for dependency in values:
                if dependency not in known_names:
                    errors.append(f"registry.skills[{index}].dependencies.{field}: unknown skill '{dependency}'")

    return errors


def load_registry(
    repo_root: Path,
    registry_path: Path | None = None,
    *,
    require_paths: bool = True,
) -> SkillRegistry:
    """Load the one authoritative registry or raise ``RegistryError``."""

    repo_root = repo_root.resolve()
    path = (registry_path or repo_root / REGISTRY_RELATIVE_PATH).resolve()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise RegistryError(f"{path}: {error}") from error
    errors = validate_registry_data(data, repo_root, require_paths=require_paths)
    if errors:
        raise RegistryError("\n".join(errors))
    return SkillRegistry(repo_root, path, data, tuple(data["skills"]))


def identity_set(records: Iterable[dict[str, Any]]) -> set[str]:
    """Return names and aliases for compatibility checks."""

    return {
        identity
        for record in records
        for identity in (record["name"], *record["aliases"])
    }
