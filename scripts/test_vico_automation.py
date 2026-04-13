#!/usr/bin/env python3
from __future__ import annotations

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
EXEC_RUNNER_REF = SKILLS_ROOT / "vico-exec" / "references" / "runner.md"
EXEC_CC_OPERATOR = SKILLS_ROOT / "vico-exec" / "references" / "cc-operator.md"
EXPORT_UTIL = SKILLS_ROOT / "scripts" / "export_vico_operating_md.py"
FEEDBACK_SKILL = SKILLS_ROOT / "vico-feedback" / "SKILL.md"
FEEDBACK_HELP = SKILLS_ROOT / "vico-feedback" / "references" / "help-template.md"
README = SKILLS_ROOT / "README.md"
README_ZH = SKILLS_ROOT / "README-zh.md"
CONSENSUS = SKILLS_ROOT / "CONSENSUS.md"
CONSENSUS_ZH = SKILLS_ROOT / "CONSENSUS-zh.md"


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

        self.assertIn("`vico-ground`", readme)
        self.assertNotIn("`vico-probe`:", readme)
        self.assertNotIn("`vico-grill`:", readme)
        self.assertIn(
            "problem framing and execution structure are separate escalation axes",
            readme,
        )
        self.assertIn("## Forward-Only Design", readme)
        self.assertIn(
            "default to forward design; do not assume historical burden", readme
        )
        self.assertIn("### Escalation Map", readme)
        self.assertIn("Horizontal axis: problem-framing rigor", readme)
        self.assertIn("Vertical axis: execution structure", readme)
        self.assertIn("Codex: vico-plan -> Claude Code: vico-exec", readme)
        self.assertIn(
            "python vico-skills/scripts/export_vico_operating_md.py AGENTS.md",
            readme,
        )
        self.assertIn("Consensus guide: [CONSENSUS.md](CONSENSUS.md)", readme)
        self.assertIn("forrestchang/andrej-karpathy-skills", readme)
        self.assertIn("## Start Here", readme)
        self.assertIn("Three common paths", readme)

        self.assertIn("`vico-ground`", readme_zh)
        self.assertIn("## 前向设计原则", readme_zh)
        self.assertIn("默认按前向设计处理，不预设历史负担", readme_zh)
        self.assertIn("问题澄清强度和执行结构强度是两条独立的升级轴", readme_zh)
        self.assertIn("### 升级坐标图", readme_zh)
        self.assertIn("Codex: vico-plan -> Claude Code: vico-exec", readme_zh)
        self.assertIn(
            "python vico-skills/scripts/export_vico_operating_md.py AGENTS.md",
            readme_zh,
        )
        self.assertIn("共识模型参考: [CONSENSUS-zh.md](CONSENSUS-zh.md)", readme_zh)
        self.assertIn("## 从这里开始", readme_zh)
        self.assertIn("三条最常见路径", readme_zh)

    def test_ground_skill_has_shared_ground_model_and_moves(self) -> None:
        ground_skill = self.read(GROUND_SKILL)
        ground_help = self.read(GROUND_HELP)
        ground_output = self.read(GROUND_OUTPUT)

        self.assertIn("lightweight grounding controller", ground_skill)
        self.assertIn(
            "Build just enough shared ground to choose a safe next route.", ground_skill
        )
        self.assertIn("## Public Moves", ground_skill)
        self.assertIn("`scan`", ground_skill)
        self.assertIn("`clarify`", ground_skill)
        self.assertIn("`stress`", ground_skill)
        self.assertIn("`handoff`", ground_skill)
        self.assertIn("## Controller Rules", ground_skill)
        self.assertIn(
            "Choose the smallest move that resolves the highest-value uncertainty.",
            ground_skill,
        )
        self.assertIn("## Stop Rule", ground_skill)
        self.assertIn(
            "Never continue grounding just to make the output look more complete.",
            ground_skill,
        )
        self.assertIn("## Minimal State Model", ground_skill)
        self.assertIn("`Facts`", ground_skill)
        self.assertIn("`Assumptions`", ground_skill)
        self.assertIn("`Tensions`", ground_skill)
        self.assertIn("`Next route`", ground_skill)
        self.assertIn("## Output Contract", ground_skill)
        self.assertIn("`Conclusion`", ground_skill)
        self.assertIn("`Evidence`", ground_skill)
        self.assertIn("`Next action`", ground_skill)
        self.assertIn("Ground Handoff", ground_skill)

        self.assertIn("## Vico Ground Help", ground_help)
        self.assertIn("- `scan`", ground_help)
        self.assertIn("- `clarify`", ground_help)
        self.assertIn("- `stress`", ground_help)
        self.assertIn("- `handoff`", ground_help)
        self.assertIn("- `Next route`", ground_help)
        self.assertIn("- `Next action`", ground_help)
        self.assertIn("Skill route: vico-ground", ground_help)
        self.assertIn(
            "Route reason: <explicit_skill_request | intent_cluster | natural_trigger>",
            ground_help,
        )
        self.assertIn(
            "Route detail: <repo_orientation | architecture_scan | exact trigger phrase>",
            ground_help,
        )
        self.assertIn("Route mode: <scan | clarify | stress | handoff>", ground_help)

        self.assertIn("# Vico Ground Output Format", ground_output)
        self.assertIn("## Scan Example", ground_output)
        self.assertIn("## Handoff Example", ground_output)
        self.assertIn("Conclusion", ground_output)
        self.assertIn("Evidence", ground_output)
        self.assertIn("Next route", ground_output)
        self.assertIn("Next action", ground_output)
        self.assertIn("## Full Handoff Example", ground_output)

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

    def test_plan_skill_consumes_ground_handoff_and_export_mode(self) -> None:
        plan_skill = self.read(PLAN_SKILL)
        plan_help = self.read(PLAN_HELP)
        handoff_template = self.read(GROUND_HANDOFF_TEMPLATE)

        self.assertIn("`vico-ground` handoff", plan_skill)
        self.assertIn("turn grounded decisions into an executable plan", plan_skill)
        self.assertIn("Treat a ground handoff as matching only when", plan_skill)
        self.assertIn("## Simplicity Discipline", plan_skill)
        self.assertIn("## Forward-Only Planning Discipline", plan_skill)
        self.assertIn("Skill route: vico-plan", plan_skill)
        self.assertIn(
            "Route reason: <explicit_skill_request | intent_cluster | natural_trigger>",
            plan_skill,
        )
        self.assertIn(
            "Route detail: <tracked_work_controller | verify_request | exact trigger phrase>",
            plan_skill,
        )

        self.assertIn("Skill route: vico-plan", plan_help)
        self.assertIn(
            "Route reason: <explicit_skill_request | intent_cluster | natural_trigger>",
            plan_help,
        )
        self.assertIn(
            "Route detail: <tracked_work_controller | verify_request | exact trigger phrase>",
            plan_help,
        )

        self.assertIn("# Ground Handoff Template", handoff_template)
        self.assertIn("Move: handoff", handoff_template)
        self.assertIn("## Ground Handoff", handoff_template)
        self.assertIn("What is true now", handoff_template)
        self.assertIn("What is still unresolved", handoff_template)
        self.assertIn("Suggested first step", handoff_template)
        self.assertIn("Optional: Tracking hint", handoff_template)
        self.assertIn("strong downstream inputs", handoff_template)
        self.assertIn("soft context inputs", handoff_template)

    def test_exec_skill_has_cc_mode_runner_and_disciplines(self) -> None:
        exec_skill = self.read(EXEC_SKILL)
        exec_help = self.read(EXEC_HELP)
        exec_automation = self.read(EXEC_AUTOMATION)
        runner_script = self.read(EXEC_RUNNER)
        runner_ref = self.read(EXEC_RUNNER_REF)
        cc_operator = self.read(EXEC_CC_OPERATOR)

        self.assertIn("`cc`", exec_skill)
        self.assertIn("launch the bundled Claude Code runner loop", exec_skill)
        self.assertIn("## Surgical Execution Discipline", exec_skill)
        self.assertIn("## Success Criteria Discipline", exec_skill)
        self.assertIn("Loop until verified", exec_skill)
        self.assertIn("Skill route: vico-exec", exec_skill)
        self.assertIn(
            "Route reason: <explicit_skill_request | intent_cluster | natural_trigger>",
            exec_skill,
        )
        self.assertIn(
            "Route detail: <persistent_implementation | continue_until_complete | exact trigger phrase>",
            exec_skill,
        )
        self.assertIn(
            "`done` requires both implementation evidence and verification evidence.",
            exec_skill,
        )

        self.assertIn("## Modes", exec_help)
        self.assertIn("- cc", exec_help)
        self.assertIn("vico-exec cc", exec_help)
        self.assertIn("run this with cc", exec_help)
        self.assertIn("handoff to cc", exec_help)
        self.assertIn("Skill route: vico-exec", exec_help)
        self.assertIn(
            "Route reason: <explicit_skill_request | intent_cluster | natural_trigger>",
            exec_help,
        )
        self.assertIn(
            "Route detail: <persistent_implementation | continue_until_complete | exact trigger phrase>",
            exec_help,
        )
        self.assertIn("Route mode: <default | cc | help>", exec_help)

        self.assertIn("## Claude Runner Loop", exec_automation)
        self.assertIn("claude_exec_runner.py", exec_automation)

        self.assertIn("RUNNER_SCHEMA", runner_script)
        self.assertIn("stale_plan", runner_script)
        self.assertIn("claude", runner_script)

        self.assertIn("## Claude Runner", runner_ref)
        self.assertIn("continue", runner_ref)
        self.assertIn("stale_plan", runner_ref)
        self.assertIn("cc-operator.md", runner_ref)

        self.assertIn("## When To Use `vico-exec cc`", cc_operator)
        self.assertIn("## Exit Codes", cc_operator)
        self.assertIn("## Recommended Operator Flow", cc_operator)
        self.assertIn("`0`", cc_operator)
        self.assertIn("`4`", cc_operator)
        self.assertIn("## Hook Vs Runner", cc_operator)
        self.assertIn("## Example Outcomes", cc_operator)

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
        self.assertIn("GitHub issue draft", feedback_skill)
        self.assertIn("how do I use vico-feedback", feedback_skill)
        self.assertIn("Skill route: vico-feedback", feedback_skill)
        self.assertIn(
            "Route reason: <explicit_skill_request | intent_cluster | natural_trigger>",
            feedback_skill,
        )
        self.assertIn(
            "Route detail: <workflow_feedback | issue_draft_request | exact trigger phrase>",
            feedback_skill,
        )
        self.assertIn("## Vico Feedback Help", feedback_help)
        self.assertIn("Skill route: vico-feedback", feedback_help)
        self.assertIn(
            "Route reason: <explicit_skill_request | intent_cluster | natural_trigger>",
            feedback_help,
        )

    def test_consensus_docs_exist_and_cover_major_theories(self) -> None:
        consensus = self.read(CONSENSUS)
        consensus_zh = self.read(CONSENSUS_ZH)

        self.assertIn("# Consensus Models", consensus)
        self.assertIn("### Common Ground", consensus)
        self.assertIn("### Conversational Grounding", consensus)
        self.assertIn("### Sensemaking", consensus)
        self.assertIn("### Collaborative Problem Solving", consensus)
        self.assertIn("### Deliberation And Argumentation", consensus)
        self.assertIn("## Practical Consensus Moves", consensus)
        self.assertIn("## Theory To Move Mapping", consensus)
        self.assertIn(
            "| Theory family | Main failure it helps with | Best Vico move | Typical artifact |",
            consensus,
        )
        self.assertIn("## Failure Patterns", consensus)
        self.assertIn("## Anti-Patterns", consensus)
        self.assertIn("clarify", consensus)
        self.assertIn("stress", consensus)

        self.assertIn("# 共识模型", consensus_zh)
        self.assertIn("### Common Ground", consensus_zh)
        self.assertIn("### Conversational Grounding", consensus_zh)
        self.assertIn("### Sensemaking", consensus_zh)
        self.assertIn("## 可用的共识动作", consensus_zh)
        self.assertIn("## 理论到 Move 的映射表", consensus_zh)
        self.assertIn("## 失败模式", consensus_zh)
        self.assertIn("## 反模式", consensus_zh)
        self.assertIn("stress", consensus_zh)


if __name__ == "__main__":
    unittest.main()
