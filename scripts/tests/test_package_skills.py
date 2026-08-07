from __future__ import annotations

import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from types import SimpleNamespace


SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

from package_skills import PackagingError, dependency_closure, package_skills  # noqa: E402


class PackageSkillsTests(unittest.TestCase):
    def make_skills(self) -> tuple[tempfile.TemporaryDirectory[str], Path, Path]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        skills = root / "skills"
        output = root / "output"
        skill = skills / "sample-skill"
        (skill / "scripts" / "__pycache__").mkdir(parents=True)
        (skill / "SKILL.md").write_text("# Sample\n", encoding="utf-8")
        (skill / "REFERENCE.md").write_text("# Reference\n", encoding="utf-8")
        (skill / "scripts" / "tool.py").write_text("print('ok')\n", encoding="utf-8")
        (skill / "scripts" / "__pycache__" / "tool.pyc").write_bytes(b"junk")
        registry = {
            "schema_version": 1,
            "category_model": {"status": "proposed", "values": ["engineering"]},
            "invocation_policy": {
                "status": "pending-owner-review",
                "allowed_modes": ["model-visible", "user-only"],
            },
            "skills": [{
                "name": "sample-skill",
                "aliases": [],
                "category": "engineering",
                "maturity": "promoted",
                "path": "skills/sample-skill",
                "public_docs": {"path": "docs/skills/sample-skill.md", "status": "planned"},
                "invocation": {
                    "mode": "pending-owner-review",
                    "claude": "pending-owner-review",
                    "codex": "pending-owner-review",
                },
                "authority": {"mode": "executor", "source_mutation": "task-scoped", "external_actions": "none"},
                "output_root": "agent-work/{slug}/sample-skill/",
                "capabilities": {
                    "decision_tree": True,
                    "work_artifacts": True,
                    "readme_registration": True,
                    "theme_library_discovery": True,
                    "goalpro_handoff": False,
                    "quality_report": False,
                    "product_research": False,
                },
                "contracts": ["work-artifacts"],
                "dependencies": {"required_skills": [], "optional_skills": []},
                "evals": ["trigger", "artifact"],
                "tests": [],
                "distribution": {"standalone_archive": True, "stable_plugin": True, "public_install": True},
                "provenance": {"origin": "gremlin-skills", "acknowledgements": []},
                "deprecation": None,
            }],
        }
        (skills / "registry.json").write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
        (root / "package.json").write_text(
            json.dumps({"name": "gremlin-skills", "version": "0.1.0", "private": True}) + "\n",
            encoding="utf-8",
        )
        return temporary, skills, output

    def test_packages_top_level_skill_and_excludes_junk(self) -> None:
        temporary, skills, output = self.make_skills()
        self.addCleanup(temporary.cleanup)
        records = package_skills(skills, output, validate=False)
        self.assertEqual("sample-skill", records[0]["skill"])
        with zipfile.ZipFile(output / "sample-skill.zip") as bundle:
            self.assertEqual(
                [
                    "sample-skill/REFERENCE.md",
                    "sample-skill/SKILL.md",
                    "sample-skill/scripts/tool.py",
                ],
                sorted(bundle.namelist()),
            )
        manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual("0.1.0", manifest["packageVersion"])
        self.assertEqual(records, manifest["skills"])

    def test_archives_are_deterministic(self) -> None:
        temporary, skills, output = self.make_skills()
        self.addCleanup(temporary.cleanup)
        first = package_skills(skills, output, validate=False)[0]["sha256"]
        second = package_skills(skills, output, validate=False)[0]["sha256"]
        self.assertEqual(first, second)

    def test_required_dependency_closure_is_transitive_and_sorted(self) -> None:
        def record(required: list[str]) -> dict:
            return {
                "dependencies": {"required_skills": required},
                "distribution": {"standalone_archive": True},
            }

        registry = SimpleNamespace(by_name={
            "root": record(["zeta", "alpha"]),
            "alpha": record(["shared"]),
            "zeta": record(["shared"]),
            "shared": record([]),
        })
        self.assertEqual(["alpha", "root", "shared", "zeta"], dependency_closure(registry, "root"))

    def test_required_dependency_cycle_is_rejected(self) -> None:
        registry = SimpleNamespace(by_name={
            "alpha": {
                "dependencies": {"required_skills": ["beta"]},
                "distribution": {"standalone_archive": True},
            },
            "beta": {
                "dependencies": {"required_skills": ["alpha"]},
                "distribution": {"standalone_archive": True},
            },
        })
        with self.assertRaisesRegex(PackagingError, "dependency cycle: alpha -> beta -> alpha"):
            dependency_closure(registry, "alpha")

    def test_unknown_skill_fails(self) -> None:
        temporary, skills, output = self.make_skills()
        self.addCleanup(temporary.cleanup)
        with self.assertRaisesRegex(PackagingError, "unknown skill"):
            package_skills(skills, output, ["missing"], validate=False)

    def test_output_inside_skills_is_rejected(self) -> None:
        temporary, skills, _ = self.make_skills()
        self.addCleanup(temporary.cleanup)
        with self.assertRaisesRegex(PackagingError, "outside skills"):
            package_skills(skills, skills / "dist", validate=False)

    def test_unregistered_skill_source_is_rejected(self) -> None:
        temporary, skills, output = self.make_skills()
        self.addCleanup(temporary.cleanup)
        extra = skills / "unregistered"
        extra.mkdir()
        (extra / "SKILL.md").write_text("# Unregistered\n", encoding="utf-8")
        with self.assertRaisesRegex(PackagingError, "unregistered skill source"):
            package_skills(skills, output, validate=False)

    def test_clean_preserves_unrelated_archives(self) -> None:
        temporary, skills, output = self.make_skills()
        self.addCleanup(temporary.cleanup)
        output.mkdir()
        unrelated = output / "personal-backup.zip"
        unrelated.write_bytes(b"keep")
        (output / "sample-skill.zip").write_bytes(b"stale")
        package_skills(skills, output, clean=True, validate=False)
        self.assertEqual(b"keep", unrelated.read_bytes())
        self.assertNotEqual(b"stale", (output / "sample-skill.zip").read_bytes())


if __name__ == "__main__":
    unittest.main()
