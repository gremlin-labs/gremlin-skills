#!/usr/bin/env python3
"""Unit tests for Workspacepro deterministic utilities."""

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

import validate_workspace_manifest as validator
import workspace_inventory


def git(path: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(path), *args], text=True).strip()


class InventoryTests(unittest.TestCase):
    def test_remote_credentials_are_sanitized(self) -> None:
        credentialed = "https://" + "user" + ":" + "secret" + "@example.com/team/repo.git"
        self.assertEqual(
            workspace_inventory.sanitize_remote(credentialed),
            "https://example.com/team/repo.git",
        )

    def test_remote_query_fragment_and_scp_user_are_sanitized(self) -> None:
        credentialed_https = (
            "https://" + "user" + ":" + "secret" + "@example.com/team/repo.git?token=secret#credential"
        )
        credentialed_ssh = "ssh://" + "git" + ":" + "secret" + "@example.com:2222/team/repo.git"
        self.assertEqual(
            "https://example.com/team/repo.git",
            workspace_inventory.sanitize_remote(credentialed_https),
        )
        self.assertEqual(
            "ssh://example.com:2222/team/repo.git",
            workspace_inventory.sanitize_remote(credentialed_ssh),
        )
        self.assertEqual(
            "github.com:team/repo.git",
            workspace_inventory.sanitize_remote("git@github.com:team/repo.git"),
        )

    def test_main_and_linked_worktrees_are_discovered(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            main = root / "main"
            linked = root / "linked"
            main.mkdir()
            git(main, "init", "-q")
            (main / "README.md").write_text("# Test\n", encoding="utf-8")
            git(main, "add", "README.md")
            subprocess.check_call([
                "git", "-C", str(main), "-c", "user.name=Test", "-c",
                "user.email=test@example.com", "commit", "-qm", "initial",
            ])
            git(main, "worktree", "add", "-q", "-b", "linked-branch", str(linked))
            report = workspace_inventory.inventory([main, linked], max_depth=0)
            forms = {item["git_form"] for item in report["repositories"]}
            self.assertEqual(forms, {"main-worktree", "linked-worktree"})
            self.assertEqual(report["summary"]["errors"], 0)


class ManifestTests(unittest.TestCase):
    def manifest(self) -> dict:
        return {
            "version": 1,
            "workspace": {"name": "sample", "topology": "sibling-repos"},
            "projects": [
                {
                    "name": "protocol",
                    "path": "libs/protocol",
                    "role": "library",
                    "lifecycle": "active",
                    "groups": ["core"],
                    "dependencies": [],
                },
                {
                    "name": "api",
                    "path": "services/api",
                    "role": "service",
                    "lifecycle": "active",
                    "groups": ["core"],
                    "dependencies": [{"project": "protocol", "kind": "build"}],
                },
            ],
            "shared_paths": [{"path": "docs", "kind": "documentation"}],
        }

    def test_valid_manifest_and_lock(self) -> None:
        manifest = self.manifest()
        lock = {
            "manifest_digest": validator.canonical_digest(manifest),
            "projects": {
                "protocol": {"commit": "a" * 40},
                "api": {"commit": "b" * 40},
            },
        }
        report = validator.validate(manifest, lock)
        self.assertTrue(report["valid"])
        self.assertEqual(report["summary"]["issues"], 0)

    def test_cycle_path_escape_and_stale_lock_are_rejected(self) -> None:
        manifest = self.manifest()
        manifest["projects"][0]["path"] = "../protocol"
        manifest["projects"][0]["dependencies"] = [{"project": "api", "kind": "runtime"}]
        lock = {
            "manifest_digest": "sha256:stale",
            "projects": {"obsolete": {"commit": "bad"}},
        }
        report = validator.validate(manifest, lock)
        codes = {item["code"] for item in report["issues"]}
        self.assertTrue({"PROJECT_PATH", "DEPENDENCY_CYCLE", "LOCK_DIGEST", "MISSING_LOCK", "STALE_LOCK"}.issubset(codes))

    def test_owned_project_cannot_build_from_reference(self) -> None:
        manifest = self.manifest()
        manifest["projects"][0]["role"] = "reference"
        report = validator.validate(manifest)
        self.assertIn("EDITABLE_REFERENCE_DEPENDENCY", {item["code"] for item in report["issues"]})


if __name__ == "__main__":
    unittest.main()
