from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1]
ROOT = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))

from generate_docs import DocsGenerationError, collect_updates, replace_block, replace_heading_section  # noqa: E402
from skill_registry import load_registry  # noqa: E402
from validate_docs import validate_docs  # noqa: E402


class DocumentationValidatorTests(unittest.TestCase):
    def make_repo(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        shutil.copytree(ROOT / "skills", root / "skills")
        shutil.copytree(ROOT / "docs", root / "docs")
        shutil.copytree(ROOT / "assets", root / "assets")
        for name in (
            "README.md",
            "CHANGELOG.md",
            "LICENSE",
            "CONTRIBUTING.md",
            "SECURITY.md",
            "AGENTS.md",
            "CONTEXT.md",
            "ACKNOWLEDGEMENTS.md",
            "THIRD-PARTY-NOTICES.md",
        ):
            shutil.copy2(ROOT / name, root / name)
        return temporary, root

    def assert_has_error(self, errors: list[str], phrase: str) -> None:
        self.assertTrue(any(phrase in error for error in errors), errors)

    def test_current_public_docs_are_valid(self) -> None:
        self.assertEqual([], validate_docs(ROOT, load_registry(ROOT)))

    def test_generated_block_replacement_preserves_curated_prose(self) -> None:
        source = "Before\n<!-- BEGIN GENERATED:SKILL-INDEX -->\nold\n<!-- END GENERATED:SKILL-INDEX -->\nAfter\n"
        result = replace_block(source, "skill-index", "new")
        self.assertEqual(
            "Before\n<!-- BEGIN GENERATED:SKILL-INDEX -->\nnew\n<!-- END GENERATED:SKILL-INDEX -->\nAfter\n",
            result,
        )
        with self.assertRaises(DocsGenerationError):
            replace_block("no markers", "skill-index", "new")

    def test_heading_section_replacement_needs_no_html_markers(self) -> None:
        source = "Before\n## Catalog\nold\n\n## Next\nAfter\n"
        result = replace_heading_section(source, "## Catalog", "## Next", "new")
        self.assertEqual("Before\n## Catalog\n\nnew\n\n## Next\nAfter\n", result)
        self.assertNotIn("<!--", result)
        with self.assertRaises(DocsGenerationError):
            replace_heading_section("## Catalog\nold\n", "## Catalog", "## Next", "new")
        with self.assertRaises(DocsGenerationError):
            replace_heading_section(source + source, "## Catalog", "## Next", "new")

    def test_missing_header_image_fails(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        readme = root / "README.md"
        readme.write_text(readme.read_text().replace("assets/gremlinlabs-gremlin-skills.jpg", "missing.jpg"), encoding="utf-8")
        self.assert_has_error(validate_docs(root, load_registry(root)), "missing Gremlin Skills header image")

    def test_missing_acknowledgements_link_fails(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        readme = root / "README.md"
        readme.write_text(
            readme.read_text().replace("[acknowledgements](ACKNOWLEDGEMENTS.md)", "acknowledgements"),
            encoding="utf-8",
        )
        self.assert_has_error(validate_docs(root, load_registry(root)), "expected one concise acknowledgements link")

    def test_missing_promoted_page_fails(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        (root / "docs" / "skills" / "audit-compare.md").unlink()
        registry = load_registry(root, require_paths=False)
        self.assert_has_error(validate_docs(root, registry), "missing human doc")

    def test_stale_generated_block_fails(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        page = root / "docs" / "skills" / "audit-compare.md"
        page.write_text(page.read_text().replace("`engineering`", "`growth`", 1), encoding="utf-8")
        self.assert_has_error(validate_docs(root, load_registry(root)), "generated registry block is stale")

    def test_broken_local_link_fails(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        page = root / "docs" / "skills" / "audit-compare.md"
        page.write_text(page.read_text() + "\n[Missing](missing.md)\n", encoding="utf-8")
        self.assert_has_error(validate_docs(root, load_registry(root)), "broken local link")

    def test_notice_index_must_cover_skill_local_notices(self) -> None:
        temporary, root = self.make_repo()
        self.addCleanup(temporary.cleanup)
        notices = root / "THIRD-PARTY-NOTICES.md"
        notices.write_text(
            notices.read_text().replace(
                "skills/experience/gamepro/THIRD-PARTY-NOTICES.md",
                "removed",
            ),
            encoding="utf-8",
        )
        self.assert_has_error(validate_docs(root, load_registry(root)), "missing notice index entry")

    def test_repository_generated_blocks_are_current(self) -> None:
        updates = collect_updates(ROOT, load_registry(ROOT))
        self.assertTrue(updates)
        self.assertTrue(all(path.read_text(encoding="utf-8") == content for path, content in updates.items()))


if __name__ == "__main__":
    unittest.main()
