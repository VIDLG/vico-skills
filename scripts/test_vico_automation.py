#!/usr/bin/env python3
from __future__ import annotations

import ast
import json
import shutil
import subprocess
import sys
import unittest
import uuid
from pathlib import Path


SKILLS_ROOT = Path(__file__).resolve().parents[1]
PLAN_SCRIPTS = SKILLS_ROOT / "vico-plan" / "scripts"
PLAN_BOOTSTRAP_SCRIPT = PLAN_SCRIPTS / "bootstrap_vico_slug.py"
HEADERS_SCRIPT = PLAN_SCRIPTS / "sync_vico_headers.py"
INDEX_SCRIPT = PLAN_SCRIPTS / "sync_vico_index.py"
CLOSE_SCRIPT = PLAN_SCRIPTS / "close_vico_slug.py"
WORKSPACE_VALIDATE_SCRIPT = PLAN_SCRIPTS / "validate_vico_workspace.py"
RUNTIME_CLI_ROOT = SKILLS_ROOT / "runtime" / "cli"
RUNTIME_BOOTSTRAP_SCRIPT = RUNTIME_CLI_ROOT / "bootstrap_vico_slug.py"
RUNTIME_HEADERS_SCRIPT = RUNTIME_CLI_ROOT / "sync_vico_headers.py"
RUNTIME_INDEX_SCRIPT = RUNTIME_CLI_ROOT / "sync_vico_index.py"
RUNTIME_CLOSE_SCRIPT = RUNTIME_CLI_ROOT / "close_vico_slug.py"
RUNTIME_WORKSPACE_VALIDATE_SCRIPT = RUNTIME_CLI_ROOT / "validate_vico_workspace.py"
GROUND_SKILL = SKILLS_ROOT / "vico-ground" / "SKILL.md"
GROUND_HELP = SKILLS_ROOT / "vico-ground" / "references" / "help-template.md"
GROUND_OUTPUT = SKILLS_ROOT / "vico-ground" / "references" / "output-format.md"
PLAN_SKILL = SKILLS_ROOT / "vico-plan" / "SKILL.md"
PLAN_HELP = SKILLS_ROOT / "vico-plan" / "references" / "templates" / "help-template.md"
PLAN_REVIEW = (
    SKILLS_ROOT / "vico-plan" / "references" / "templates" / "review-template.md"
)
PLAN_VERIFY = (
    SKILLS_ROOT / "vico-plan" / "references" / "templates" / "verify-template.md"
)
PLAN_TRUTH = (
    SKILLS_ROOT / "vico-plan" / "references" / "templates" / "truth-template.md"
)
GROUND_HANDOFF_TEMPLATE = (
    SKILLS_ROOT
    / "vico-plan"
    / "references"
    / "templates"
    / "ground-handoff-template.md"
)
EXEC_SKILL = SKILLS_ROOT / "vico-exec" / "SKILL.md"
EXEC_HELP = SKILLS_ROOT / "vico-exec" / "references" / "help-template.md"
EXEC_AUTOMATION = SKILLS_ROOT / "vico-exec" / "references" / "automation.md"
EXEC_RUNNER = SKILLS_ROOT / "vico-exec" / "scripts" / "claude_exec_runner.py"
CLAUDE_ADAPTER_RUNNER = SKILLS_ROOT / "adapters" / "claude" / "claude_exec_runner.py"
CLAUDE_ADAPTER_SESSION_HOOK = SKILLS_ROOT / "adapters" / "claude" / "session_start_hook.ps1"
CLAUDE_ADAPTER_STOP_HOOK = SKILLS_ROOT / "adapters" / "claude" / "stop_hook.ps1"
EXEC_RUNNER_REF = SKILLS_ROOT / "vico-exec" / "references" / "runner.md"
EXEC_CC_OPERATOR = SKILLS_ROOT / "vico-exec" / "references" / "cc-operator.md"
EXPORT_UTIL = SKILLS_ROOT / "scripts" / "export_vico_operating_md.py"
OPENAI_AGENT_SYNC = SKILLS_ROOT / "scripts" / "sync_openai_agents.py"
SHARED_RUNTIME_SYNC = SKILLS_ROOT / "scripts" / "sync_shared_vico_runtime.py"
FEEDBACK_SKILL = SKILLS_ROOT / "vico-feedback" / "SKILL.md"
FEEDBACK_HELP = SKILLS_ROOT / "vico-feedback" / "references" / "help-template.md"
OPS_SKILL = SKILLS_ROOT / "vico-ops" / "SKILL.md"
OPS_HELP = SKILLS_ROOT / "vico-ops" / "references" / "help-template.md"
README = SKILLS_ROOT / "README.md"
README_ZH = SKILLS_ROOT / "README-zh.md"
CONSENSUS = SKILLS_ROOT / "CONSENSUS.md"
CONSENSUS_ZH = SKILLS_ROOT / "CONSENSUS-zh.md"
SHARED_VICO_COMMON = SKILLS_ROOT / "runtime" / "vico_artifacts" / "vico_common.py"


def run_ok(*args: str) -> subprocess.CompletedProcess[str]:
    result = subprocess.run([sys.executable, *args], text=True, capture_output=True)
    if result.returncode != 0:
        raise AssertionError(
            f"Command failed: {' '.join(args)}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


class VicoAutomationTests(unittest.TestCase):
    def read(self, path: Path) -> str:
        return path.read_text(encoding="utf-8")

    def normalize_script_for_parity(self, text: str) -> str:
        return ast.dump(ast.parse(text), include_attributes=False)

    def assert_contains_all(self, text: str, markers: list[str]) -> None:
        for marker in markers:
            self.assertIn(marker, text)

    def make_repo(self) -> Path:
        temp_root = SKILLS_ROOT / ".tmp-tests"
        temp_root.mkdir(exist_ok=True)
        temp_dir = temp_root / f"vico-automation-{uuid.uuid4().hex[:8]}"
        temp_dir.mkdir()
        self.addCleanup(shutil.rmtree, temp_dir, ignore_errors=True)
        (temp_dir / ".vico").mkdir()
        (temp_dir / "docs" / "architecture").mkdir(parents=True)
        return temp_dir

    def dated_slug(self, date: str, slug: str) -> str:
        return f"{date}-{slug}"

    def test_bootstrap_plan_only_creates_plan_and_index(self) -> None:
        root = self.make_repo()
        date = "2026-04-09"
        slug = self.dated_slug(date, "tiny-fix")
        run_ok(
            str(PLAN_BOOTSTRAP_SCRIPT),
            "tiny-fix",
            "Tiny Fix",
            "--repo-root",
            str(root),
            "--date",
            date,
        )

        plan = root / ".vico" / "plans" / "active" / f"{slug}.md"
        index = root / ".vico" / "index" / f"{slug}.json"
        self.assertTrue(plan.exists())
        self.assertTrue(index.exists())

        plan_text = plan.read_text(encoding="utf-8")
        self.assertIn("> Mode: `plan_only`", plan_text)
        self.assertIn(f"> Slug: `{slug}`", plan_text)

        manifest = json.loads(index.read_text(encoding="utf-8"))
        self.assertEqual(manifest["state"]["tracking_mode"], "plan_only")

    def test_sync_headers_repairs_manifest_and_crosslinks(self) -> None:
        root = self.make_repo()
        date = "2026-04-09"
        slug = self.dated_slug(date, "sync-me")
        run_ok(
            str(PLAN_BOOTSTRAP_SCRIPT),
            "sync-me",
            "Sync Me",
            "--repo-root",
            str(root),
            "--level",
            "prd_backed",
            "--no-index",
            "--date",
            date,
        )
        run_ok(str(INDEX_SCRIPT), slug, "--repo-root", str(root))
        run_ok(str(HEADERS_SCRIPT), slug, "--repo-root", str(root))

        plan_text = (root / ".vico" / "plans" / "active" / f"{slug}.md").read_text(
            encoding="utf-8"
        )
        self.assertIn(f"> Manifest: `.vico/index/{slug}.json`", plan_text)

    def test_close_slug_dry_run_surfaces_reason_and_does_not_mutate_files(self) -> None:
        root = self.make_repo()
        date = "2026-04-09"
        slug = self.dated_slug(date, "cancel-me")
        run_ok(
            str(PLAN_BOOTSTRAP_SCRIPT),
            "cancel-me",
            "Cancel Me",
            "--repo-root",
            str(root),
            "--date",
            date,
        )

        plan = root / ".vico" / "plans" / "active" / f"{slug}.md"
        before = plan.read_text(encoding="utf-8")
        result = run_ok(
            str(CLOSE_SCRIPT),
            slug,
            "--repo-root",
            str(root),
            "--reason",
            "cancel",
            "--dry-run",
        )
        self.assertIn("[dry-run] reason=cancel", result.stdout)
        self.assertEqual(plan.read_text(encoding="utf-8"), before)

    def test_workspace_validator_passes_on_bootstrapped_repo(self) -> None:
        root = self.make_repo()
        date = "2026-04-09"
        run_ok(
            str(PLAN_BOOTSTRAP_SCRIPT),
            "validated-work",
            "Validated Work",
            "--repo-root",
            str(root),
            "--level",
            "prd_backed",
            "--date",
            date,
        )
        run_ok(str(WORKSPACE_VALIDATE_SCRIPT), "--repo-root", str(root))

    def test_export_md_writes_repo_operating_brief(self) -> None:
        root = self.make_repo()
        date = "2026-04-09"
        slug = self.dated_slug(date, "export-me")
        run_ok(
            str(PLAN_BOOTSTRAP_SCRIPT),
            "export-me",
            "Export Me",
            "--repo-root",
            str(root),
            "--date",
            date,
        )
        run_ok(str(EXPORT_UTIL), "AGENTS.md", "--repo-root", str(root))
        exported = (root / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("## Vico Operating Brief", exported)
        self.assertIn("## Clarification Discipline", exported)
        self.assertIn("## Simplicity Discipline", exported)
        self.assertIn("## Surgical Edit Discipline", exported)
        self.assertIn("## Success Criteria Discipline", exported)
        self.assertIn(f"- Active slug: `{slug}`", exported)

    def test_readme_expresses_grounding_and_execution_model(self) -> None:
        readme = self.read(README)
        readme_zh = self.read(README_ZH)

        self.assert_contains_all(
            readme,
            [
                "# vico-skills",
                "## Start Here",
                "## Forward-Only Design",
                "### Escalation Map",
                "Codex: vico-plan -> Claude Code: vico-exec",
                "`vico-ops`",
                "python vico-skills/scripts/export_vico_operating_md.py AGENTS.md",
            ],
        )
        self.assertNotIn("`vico-probe`:", readme)
        self.assertNotIn("`vico-grill`:", readme)

        self.assert_contains_all(
            readme_zh,
            [
                "# vico-skills",
                "## 从这里开始",
                "## 前向设计原则",
                "### 升级坐标图",
                "Codex: vico-plan -> Claude Code: vico-exec",
                "`vico-ops`",
                "python vico-skills/scripts/export_vico_operating_md.py AGENTS.md",
            ],
        )

    def test_ground_skill_has_shared_ground_model_and_moves(self) -> None:
        ground_skill = self.read(GROUND_SKILL)
        ground_help = self.read(GROUND_HELP)
        ground_output = self.read(GROUND_OUTPUT)

        self.assert_contains_all(
            ground_skill,
            [
                "## Agent Summary",
                "## Public Moves",
                "## Controller Rules",
                "## Stop Rule",
                "## Minimal State Model",
                "## Output Contract",
                "## Full Handoff Contract",
            ],
        )
        self.assert_contains_all(
            ground_help,
            [
                "## Vico Ground Help",
                "- `scan`",
                "- `Recommended next action`",
                "Skill route: vico-ground",
            ],
        )
        self.assert_contains_all(
            ground_output,
            [
                "# Vico Ground Output Format",
                "## Scan Example",
                "## Handoff Example",
                "Recommended next action",
                "## Full Handoff Example",
            ],
        )

    def test_shared_vico_common_script_stays_in_parity(self) -> None:
        owner_tree = self.normalize_script_for_parity(self.read(SHARED_VICO_COMMON))
        for closure in (
            SKILLS_ROOT / "vico-plan" / "scripts" / "vico_common.py",
            SKILLS_ROOT / "vico-exec" / "scripts" / "vico_common.py",
        ):
            self.assertEqual(
                owner_tree,
                self.normalize_script_for_parity(self.read(closure)),
            )

    def test_export_utility_is_repo_level_not_ground_move(self) -> None:
        export_util = self.read(EXPORT_UTIL)
        ground_skill = self.read(GROUND_SKILL)

        self.assertIn(
            "Export a repo-local Vico operating brief to AGENTS.md or CLAUDE.md.",
            export_util,
        )
        self.assertIn("## Vico Operating Brief", export_util)
        self.assertIn(
            "Use `vico-ground scan`, `clarify`, `stress`, and `handoff` as the primary public moves.",
            export_util,
        )
        self.assertNotIn("`export-md` remains a utility action", ground_skill)
        self.assertNotIn("vico-ground export-md", ground_skill)

    def test_shared_runtime_sync_script_reports_clean_repo(self) -> None:
        run_ok(str(SHARED_RUNTIME_SYNC), "--root", str(SKILLS_ROOT), "--check")

    def test_openai_agent_sync_script_reports_clean_repo(self) -> None:
        run_ok(str(OPENAI_AGENT_SYNC), "--root", str(SKILLS_ROOT), "--check")

    def test_plan_cli_wrappers_delegate_to_runtime_cli_owners(self) -> None:
        wrappers = {
            PLAN_BOOTSTRAP_SCRIPT: "runtime/cli/bootstrap_vico_slug.py",
            HEADERS_SCRIPT: "runtime/cli/sync_vico_headers.py",
            INDEX_SCRIPT: "runtime/cli/sync_vico_index.py",
            CLOSE_SCRIPT: "runtime/cli/close_vico_slug.py",
            WORKSPACE_VALIDATE_SCRIPT: "runtime/cli/validate_vico_workspace.py",
        }
        for path, owner in wrappers.items():
            text = self.read(path)
            self.assertIn("runpy.run_path", text)
            self.assertIn(owner, text)

    def test_plan_skill_consumes_ground_handoff_and_export_mode(self) -> None:
        plan_skill = self.read(PLAN_SKILL)
        plan_help = self.read(PLAN_HELP)
        handoff_template = self.read(GROUND_HANDOFF_TEMPLATE)

        self.assert_contains_all(
            plan_skill,
            [
                "## Agent Summary",
                "## Simplicity Discipline",
                "## Forward-Only Planning Discipline",
                "`vico-ground` handoff",
                "Skill route: vico-plan",
            ],
        )
        self.assert_contains_all(
            plan_help,
            [
                "Skill route: vico-plan",
                "Route detail: <tracked_work_controller | verify_request | exact trigger phrase>",
                "- review",
                "- verify",
                "- replan",
            ],
        )
        self.assert_contains_all(
            handoff_template,
            [
                "# Ground Handoff Template",
                "Move: handoff",
                "## Ground Handoff",
                "What is true now",
                "Suggested first step",
            ],
        )

    def test_exec_skill_has_cc_mode_runner_and_disciplines(self) -> None:
        exec_skill = self.read(EXEC_SKILL)
        exec_help = self.read(EXEC_HELP)
        exec_automation = self.read(EXEC_AUTOMATION)
        runner_script = self.read(EXEC_RUNNER)
        adapter_runner = self.read(CLAUDE_ADAPTER_RUNNER)
        session_hook = self.read(CLAUDE_ADAPTER_SESSION_HOOK)
        stop_hook = self.read(CLAUDE_ADAPTER_STOP_HOOK)
        runner_ref = self.read(EXEC_RUNNER_REF)
        cc_operator = self.read(EXEC_CC_OPERATOR)

        self.assert_contains_all(
            exec_skill,
            [
                "## Agent Summary",
                "## Surgical Execution Discipline",
                "## Success Criteria Discipline",
                "## Claude Code",
                "Loop until verified",
                "Claude-specific owner sources live under `adapters/claude/`",
            ],
        )
        self.assert_contains_all(
            exec_help,
            [
                "## Modes",
                "- cc",
                "vico-exec cc",
                "Skill route: vico-exec",
            ],
        )
        self.assert_contains_all(
            exec_automation,
            [
                "## Claude Runner Loop",
                "claude_exec_runner.py",
            ],
        )

        self.assertIn("runpy.run_path", runner_script)
        self.assertIn("adapters", runner_script)
        self.assertIn("RUNNER_SCHEMA", adapter_runner)
        self.assertIn("stale_plan", adapter_runner)
        self.assertIn("claude", adapter_runner)
        self.assertIn("active plans detected", session_hook)
        self.assertIn("active in-progress plan still exists", stop_hook)

        self.assert_contains_all(
            runner_ref,
            ["## Claude Runner", "continue", "stale_plan", "cc-operator.md"],
        )
        self.assert_contains_all(
            cc_operator,
            [
                "## When To Use `vico-exec cc`",
                "## Exit Codes",
                "## Recommended Operator Flow",
                "## Hook Vs Runner",
            ],
        )

        plan_review = self.read(PLAN_REVIEW)
        plan_verify = self.read(PLAN_VERIFY)
        exec_report = self.read(
            SKILLS_ROOT / "vico-exec" / "references" / "execution-report-template.md"
        )
        self.assertIn("Confidence: high | medium | low", plan_review)
        self.assertIn(
            "Scope impact: local | active_slug | cross_slug | repo_wide", plan_review
        )
        self.assertIn("Uncertainty source:", plan_review)
        self.assertIn("## Risk If Skipped", plan_review)
        self.assertIn("## Alternative Next Steps", plan_review)
        self.assertIn("Confidence: high | medium | low", plan_verify)
        self.assertIn(
            "Scope impact: local | active_slug | cross_slug | repo_wide", plan_verify
        )
        self.assertIn("Uncertainty source:", plan_verify)
        self.assertIn("## Risk If Skipped", plan_verify)
        self.assertIn("## Alternative Next Modes", plan_verify)
        self.assertIn("Confidence: high | medium | low", exec_report)
        self.assertIn(
            "Scope impact: local | active_slug | cross_slug | repo_wide", exec_report
        )
        self.assertIn("Uncertainty source:", exec_report)
        self.assertIn("## Risk If Skipped", exec_report)
        self.assertIn("## Alternative Next Steps", exec_report)

    def test_feedback_skill_is_present(self) -> None:
        feedback_skill = self.read(FEEDBACK_SKILL)
        feedback_help = self.read(FEEDBACK_HELP)
        self.assert_contains_all(
            feedback_skill,
            [
                "GitHub issue draft",
                "## Agent Summary",
                "Skill route: vico-feedback",
            ],
        )
        self.assert_contains_all(
            feedback_help,
            ["## Vico Feedback Help", "Skill route: vico-feedback"],
        )

    def test_ops_skill_is_present(self) -> None:
        ops_skill = self.read(OPS_SKILL)
        ops_help = self.read(OPS_HELP)
        self.assert_contains_all(
            ops_skill,
            [
                "## Agent Summary",
                "## Modes",
                "## Control Rules",
                "## Repo-Local Operations",
                "Skill route: vico-ops",
            ],
        )
        self.assert_contains_all(
            ops_help,
            [
                "## Vico Ops Help",
                "- bootstrap",
                "- close",
                "- validate",
                "Skill route: vico-ops",
            ],
        )

    def test_consensus_docs_exist_and_cover_major_theories(self) -> None:
        consensus = self.read(CONSENSUS)
        consensus_zh = self.read(CONSENSUS_ZH)

        self.assert_contains_all(
            consensus,
            [
                "# Consensus Models",
                "## Practical Consensus Moves",
                "## Theory To Move Mapping",
                "## Anti-Patterns",
            ],
        )
        self.assert_contains_all(
            consensus_zh,
            [
                "# 共识模型",
                "## 可用的共识动作",
                "## 理论到 Move 的映射表",
                "## 反模式",
            ],
        )


if __name__ == "__main__":
    unittest.main()
