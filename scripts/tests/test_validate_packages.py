from __future__ import annotations

import hashlib
import json
import shutil
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1]
ROOT = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))

from materialize_contracts import write_materialized  # noqa: E402
from package_skills import package_skills  # noqa: E402
from skill_registry import load_registry  # noqa: E402
from validate_packages import validate_packages  # noqa: E402


class PackageValidatorTests(unittest.TestCase):
    def make_package(self) -> tuple[tempfile.TemporaryDirectory[str], Path, Path]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name) / "repo"
        package_dir = Path(temporary.name) / "packages"
        fixture = Path(__file__).resolve().parent / "fixtures" / "valid-repo"
        shutil.copytree(fixture, root)
        shutil.copytree(ROOT / "contracts", root / "contracts")
        (root / "scripts").mkdir(exist_ok=True)
        shutil.copy2(
            ROOT / "scripts" / "validate_seo_change_control.py",
            root / "scripts" / "validate_seo_change_control.py",
        )
        registry = load_registry(root)
        write_materialized(root, registry)
        package_skills(root / "skills", package_dir, validate=False)
        return temporary, root, package_dir

    def assert_has_error(self, errors: list[str], phrase: str) -> None:
        self.assertTrue(any(phrase in error for error in errors), errors)

    def rewrite_manifest_record(self, package_dir: Path, archive: Path) -> None:
        manifest_path = package_dir / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        record = manifest["skills"][0]
        payload = archive.read_bytes()
        with zipfile.ZipFile(archive) as bundle:
            record["files"] = len(bundle.infolist())
        record["bytes"] = len(payload)
        record["sha256"] = hashlib.sha256(payload).hexdigest()
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    def test_valid_extracted_archive(self) -> None:
        temporary, root, package_dir = self.make_package()
        self.addCleanup(temporary.cleanup)
        self.assertEqual((1, []), validate_packages(root, package_dir))

    def test_checksum_tampering_fails(self) -> None:
        temporary, root, package_dir = self.make_package()
        self.addCleanup(temporary.cleanup)
        archive = package_dir / "sample-skill.zip"
        archive.write_bytes(archive.read_bytes() + b"tamper")
        self.assert_has_error(validate_packages(root, package_dir)[1], "checksum mismatch")

    def test_missing_skill_entrypoint_fails_after_valid_checksum(self) -> None:
        temporary, root, package_dir = self.make_package()
        self.addCleanup(temporary.cleanup)
        archive = package_dir / "sample-skill.zip"
        rewritten = package_dir / "rewritten.zip"
        with zipfile.ZipFile(archive) as source, zipfile.ZipFile(rewritten, "w") as target:
            for info in source.infolist():
                if info.filename != "sample-skill/SKILL.md":
                    target.writestr(info, source.read(info.filename))
        rewritten.replace(archive)
        self.rewrite_manifest_record(package_dir, archive)
        self.assert_has_error(validate_packages(root, package_dir)[1], "is missing SKILL.md")

    def test_unsafe_archive_member_fails_before_extraction(self) -> None:
        temporary, root, package_dir = self.make_package()
        self.addCleanup(temporary.cleanup)
        archive = package_dir / "sample-skill.zip"
        with zipfile.ZipFile(archive, "a") as bundle:
            bundle.writestr("../escape.txt", "bad")
        self.rewrite_manifest_record(package_dir, archive)
        self.assert_has_error(validate_packages(root, package_dir)[1], "unsafe or unscoped member")

    def test_declared_closure_drift_fails(self) -> None:
        temporary, root, package_dir = self.make_package()
        self.addCleanup(temporary.cleanup)
        manifest_path = package_dir / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["skills"][0]["closure"] = []
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        self.assert_has_error(validate_packages(root, package_dir)[1], "does not match")


if __name__ == "__main__":
    unittest.main()
