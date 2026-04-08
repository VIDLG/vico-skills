#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path
import shutil
import uuid


SKILLS_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = SKILLS_ROOT.parent
DOCS_SCRIPTS = SKILLS_ROOT / "wilco-docs" / "scripts"
INIT_SCRIPT = SKILLS_ROOT / "wilco-init" / "scripts" / "bootstrap_wilco_slug.py"
HEADERS_SCRIPT = DOCS_SCRIPTS / "sync_wilco_headers.py"
INDEX_SCRIPT = DOCS_SCRIPTS / "sync_wilco_index.py"
CLOSE_SCRIPT = DOCS_SCRIPTS / "close_wilco_slug.py"
WORKSPACE_VALIDATE_SCRIPT = DOCS_SCRIPTS / "validate_wilco_workspace.py"


def run_ok(*args: str) -> subprocess.CompletedProcess[str]:
    result = subprocess.run([sys.executable, *args], text=True, capture_output=True)
    if result.returncode != 0:
        raise AssertionError(f"Command failed: {' '.join(args)}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}")
    return result


class WilcoAutomationTests(unittest.TestCase):
    def make_repo(self) -> Path:
        temp_dir = WORKSPACE_ROOT / f"wilco-automation-{uuid.uuid4().hex[:8]}"
        temp_dir.mkdir()
        self.addCleanup(shutil.rmtree, temp_dir, ignore_errors=True)
        (temp_dir / ".wilco").mkdir()
        (temp_dir / "docs" / "architecture").mkdir(parents=True)
        return temp_dir

    def test_bootstrap_plan_only_creates_plan_and_index(self) -> None:
        root = self.make_repo()
        run_ok(str(INIT_SCRIPT), "tiny-fix", "Tiny Fix", "--repo-root", str(root))

        plan = root / ".wilco" / "plans" / "active" / "tiny-fix.md"
        index = root / ".wilco" / "index" / "tiny-fix.json"
        self.assertTrue(plan.exists())
        self.assertTrue(index.exists())
        self.assertFalse((root / ".wilco" / "prd" / "active" / "tiny-fix.md").exists())

        plan_text = plan.read_text(encoding="utf-8")
        self.assertIn("> Slug: `tiny-fix`", plan_text)
        self.assertIn("> Manifest: `.wilco/index/tiny-fix.json`", plan_text)
        self.assertNotIn("Source PRD", plan_text)

        manifest = json.loads(index.read_text(encoding="utf-8"))
        self.assertEqual(manifest["state"]["progress"], "not_started")
        self.assertEqual(manifest["artifacts"]["plan"], ".wilco/plans/active/tiny-fix.md")

    def test_bootstrap_prd_plan_arch_creates_full_initial_set(self) -> None:
        root = self.make_repo()
        run_ok(
            str(INIT_SCRIPT),
            "boundary-work",
            "Boundary Work",
            "--repo-root",
            str(root),
            "--level",
            "prd-plan-arch",
        )

        self.assertTrue((root / ".wilco" / "prd" / "active" / "boundary-work.md").exists())
        self.assertTrue((root / ".wilco" / "plans" / "active" / "boundary-work.md").exists())
        self.assertTrue((root / "docs" / "architecture" / "boundary-work.md").exists())

    def test_sync_headers_repairs_manifest_and_crosslinks(self) -> None:
        root = self.make_repo()
        run_ok(
            str(INIT_SCRIPT),
            "sync-me",
            "Sync Me",
            "--repo-root",
            str(root),
            "--level",
            "prd-plan",
            "--no-index",
        )

        run_ok(str(INDEX_SCRIPT), "sync-me", "--repo-root", str(root))
        run_ok(str(HEADERS_SCRIPT), "sync-me", "--repo-root", str(root))

        plan_text = (root / ".wilco" / "plans" / "active" / "sync-me.md").read_text(encoding="utf-8")
        prd_text = (root / ".wilco" / "prd" / "active" / "sync-me.md").read_text(encoding="utf-8")
        self.assertIn("> Manifest: `.wilco/index/sync-me.json`", plan_text)
        self.assertIn("> Source PRD: `.wilco/prd/active/sync-me.md`", plan_text)
        self.assertIn("Manifest: `.wilco/index/sync-me.json`", prd_text)
        self.assertIn("Related plan: `.wilco/plans/active/sync-me.md`", prd_text)

    def test_close_slug_archives_and_cleans(self) -> None:
        root = self.make_repo()
        run_ok(
            str(INIT_SCRIPT),
            "done-work",
            "Done Work",
            "--repo-root",
            str(root),
            "--level",
            "prd-plan",
        )
        (root / ".wilco" / "resume" / "done-work.md").write_text("## Resume Summary\n", encoding="utf-8")
        run_ok(str(INDEX_SCRIPT), "done-work", "--repo-root", str(root))
        run_ok(str(CLOSE_SCRIPT), "done-work", "--repo-root", str(root), "--completed-date", "2026-04-08")

        self.assertFalse((root / ".wilco" / "plans" / "active" / "done-work.md").exists())
        self.assertFalse((root / ".wilco" / "prd" / "active" / "done-work.md").exists())
        self.assertFalse((root / ".wilco" / "resume" / "done-work.md").exists())
        self.assertFalse((root / ".wilco" / "index" / "done-work.json").exists())
        archived_plan = (root / ".wilco" / "plans" / "archive" / "done-work.md").read_text(encoding="utf-8")
        self.assertIn("> Status: `archived`", archived_plan)

    def test_workspace_validator_passes_on_bootstrapped_repo(self) -> None:
        root = self.make_repo()
        run_ok(
            str(INIT_SCRIPT),
            "validated-work",
            "Validated Work",
            "--repo-root",
            str(root),
            "--level",
            "prd-plan",
        )
        run_ok(str(WORKSPACE_VALIDATE_SCRIPT), "--repo-root", str(root))


if __name__ == "__main__":
    unittest.main()
