from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

from generate_plugin_manifests import (  # noqa: E402
    build_plugins,
    check_openai_metadata,
    claude_skill_markdown,
    write_openai_metadata,
)
from skill_registry import load_registry  # noqa: E402
from validate_plugins import validate_plugins  # noqa: E402


class PluginGenerationTests(unittest.TestCase):
    def make_repo(self) -> tuple[tempfile.TemporaryDirectory[str], Path, Path]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name) / "repo"
        output = Path(temporary.name) / "plugins"
        fixture = Path(__file__).resolve().parent / "fixtures" / "valid-repo"
        shutil.copytree(fixture, root)
        registry_path = root / "skills" / "registry.json"
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        registry["invocation_policy"]["status"] = "approved"
        for record in registry["skills"]:
            record["invocation"] = {
                "mode": "user-only",
                "claude": "user-only",
                "codex": "user-only",
            }
        registry_path.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
        (root / "package.json").write_text(
            json.dumps({
                "name": "gremlin-skills",
                "version": "0.1.0",
                "private": True,
                "description": "A test collection of agent skills.",
                "license": "MIT",
                "author": {"name": "E.J. Coughlin", "email": "ej@gremlinlabs.com"},
                "repository": {"type": "git", "url": "git+https://github.com/gremlin-labs/gremlin-skills.git"},
                "homepage": "https://github.com/gremlin-labs/gremlin-skills#readme",
            }, indent=2) + "\n",
            encoding="utf-8",
        )
        (root / "LICENSE").write_text("MIT\n", encoding="utf-8")
        (root / "THIRD-PARTY-NOTICES.md").write_text("# Notices\n", encoding="utf-8")
        return temporary, root, output

    def test_user_only_metadata_is_native_to_each_host(self) -> None:
        temporary, root, output = self.make_repo()
        self.addCleanup(temporary.cleanup)
        registry = load_registry(root)
        write_openai_metadata(registry)
        self.assertEqual([], check_openai_metadata(registry))
        build_plugins(root, output, clean=True)
        source = root / "skills" / "sample-skill" / "SKILL.md"
        self.assertNotIn("disable-model-invocation", source.read_text(encoding="utf-8"))
        codex_yaml = output / "codex" / "gremlin-skills" / "skills" / "sample-skill" / "agents" / "openai.yaml"
        self.assertIn("allow_implicit_invocation: false", codex_yaml.read_text(encoding="utf-8"))
        claude_skill = output / "claude" / "gremlin-skills" / "skills" / "sample-skill" / "SKILL.md"
        self.assertIn("disable-model-invocation: true", claude_skill.read_text(encoding="utf-8"))
        self.assertEqual((1, []), validate_plugins(root, output))

    def test_claude_model_visible_removes_explicit_only_flag(self) -> None:
        source = "---\nname: example\ndescription: Example workflow.\ndisable-model-invocation: true\n---\n\nBody\n"
        transformed = claude_skill_markdown(source, "model-visible")
        self.assertNotIn("disable-model-invocation", transformed)

    def test_plugin_payload_tampering_fails(self) -> None:
        temporary, root, output = self.make_repo()
        self.addCleanup(temporary.cleanup)
        registry = load_registry(root)
        write_openai_metadata(registry)
        build_plugins(root, output, clean=True)
        target = output / "codex" / "gremlin-skills" / "skills" / "sample-skill" / "SKILL.md"
        target.write_text(target.read_text(encoding="utf-8") + "tamper\n", encoding="utf-8")
        errors = validate_plugins(root, output)[1]
        self.assertTrue(any("unexpected host transformation" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
