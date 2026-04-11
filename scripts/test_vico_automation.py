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
PLAN_SCRIPTS = SKILLS_ROOT / "vico-plan" / "scripts"
PLAN_BOOTSTRAP_SCRIPT = PLAN_SCRIPTS / "bootstrap_vico_slug.py"
HEADERS_SCRIPT = PLAN_SCRIPTS / "sync_vico_headers.py"
INDEX_SCRIPT = PLAN_SCRIPTS / "sync_vico_index.py"
CLOSE_SCRIPT = PLAN_SCRIPTS / "close_vico_slug.py"
WORKSPACE_VALIDATE_SCRIPT = PLAN_SCRIPTS / "validate_vico_workspace.py"
PROBE_SKILL = SKILLS_ROOT / "vico-probe" / "SKILL.md"
PROBE_HELP = SKILLS_ROOT / "vico-probe" / "references" / "help-template.md"
PROBE_OUTPUT = SKILLS_ROOT / "vico-probe" / "references" / "output-format.md"
PLAN_SKILL = SKILLS_ROOT / "vico-plan" / "SKILL.md"
PROBE_HANDOFF_TEMPLATE = SKILLS_ROOT / "vico-plan" / "references" / "templates" / "probe-handoff-template.md"
PLAN_HELP = SKILLS_ROOT / "vico-plan" / "references" / "templates" / "help-template.md"
PLAN_REVIEW = SKILLS_ROOT / "vico-plan" / "references" / "templates" / "review-template.md"
PLAN_VERIFY = SKILLS_ROOT / "vico-plan" / "references" / "templates" / "verify-template.md"
PLAN_TRUTH = SKILLS_ROOT / "vico-plan" / "references" / "templates" / "truth-template.md"
EXEC_SKILL = SKILLS_ROOT / "vico-exec" / "SKILL.md"
EXEC_HELP = SKILLS_ROOT / "vico-exec" / "references" / "help-template.md"
EXEC_AUTOMATION = SKILLS_ROOT / "vico-exec" / "references" / "automation.md"
EXEC_STATUS = SKILLS_ROOT / "vico-exec" / "references" / "status-vocabulary.md"
EXEC_SYNC_SCRIPT = SKILLS_ROOT / "vico-exec" / "scripts" / "sync_vico_index.py"
FEEDBACK_SKILL = SKILLS_ROOT / "vico-feedback" / "SKILL.md"
FEEDBACK_HELP = SKILLS_ROOT / "vico-feedback" / "references" / "help-template.md"
FEEDBACK_ISSUE = SKILLS_ROOT / "vico-feedback" / "references" / "issue-template.md"
README = SKILLS_ROOT / "README.md"
README_ZH = SKILLS_ROOT / "README-zh.md"


def run_ok(*args: str) -> subprocess.CompletedProcess[str]:
    result = subprocess.run([sys.executable, *args], text=True, capture_output=True)
    if result.returncode != 0:
        raise AssertionError(f"Command failed: {' '.join(args)}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}")
    return result


class VicoAutomationTests(unittest.TestCase):
    def read(self, path: Path) -> str:
        return path.read_text(encoding="utf-8")

    def make_repo(self) -> Path:
        temp_dir = WORKSPACE_ROOT / f"vico-automation-{uuid.uuid4().hex[:8]}"
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
        run_ok(str(PLAN_BOOTSTRAP_SCRIPT), "tiny-fix", "Tiny Fix", "--repo-root", str(root), "--date", date)

        plan = root / ".vico" / "plans" / "active" / f"{slug}.md"
        index = root / ".vico" / "index" / f"{slug}.json"
        self.assertTrue(plan.exists())
        self.assertTrue(index.exists())
        self.assertFalse((root / ".vico" / "prd" / "active" / f"{slug}.md").exists())

        plan_text = plan.read_text(encoding="utf-8")
        self.assertIn("> Mode: `plan_only`", plan_text)
        self.assertIn(f"> Slug: `{slug}`", plan_text)
        self.assertIn(f"> Manifest: `.vico/index/{slug}.json`", plan_text)
        self.assertNotIn("Source PRD", plan_text)

        manifest = json.loads(index.read_text(encoding="utf-8"))
        self.assertEqual(manifest["state"]["progress"], "not_started")
        self.assertEqual(manifest["state"]["tracking_mode"], "plan_only")
        self.assertEqual(manifest["artifacts"]["plan"], f".vico/plans/active/{slug}.md")

    def test_bootstrap_prd_plan_arch_creates_full_initial_set(self) -> None:
        root = self.make_repo()
        date = "2026-04-09"
        slug = self.dated_slug(date, "boundary-work")
        run_ok(
            str(PLAN_BOOTSTRAP_SCRIPT),
            "boundary-work",
            "Boundary Work",
            "--repo-root",
            str(root),
            "--level",
            "prd_backed_arch",
            "--date",
            date,
        )

        self.assertTrue((root / ".vico" / "prd" / "active" / f"{slug}.md").exists())
        self.assertTrue((root / ".vico" / "plans" / "active" / f"{slug}.md").exists())
        self.assertTrue((root / "docs" / "architecture" / f"{slug}.md").exists())

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

        plan_text = (root / ".vico" / "plans" / "active" / f"{slug}.md").read_text(encoding="utf-8")
        prd_text = (root / ".vico" / "prd" / "active" / f"{slug}.md").read_text(encoding="utf-8")
        self.assertIn("> Mode: `prd_backed`", plan_text)
        self.assertIn(f"> Manifest: `.vico/index/{slug}.json`", plan_text)
        self.assertIn(f"> Source PRD: `.vico/prd/active/{slug}.md`", plan_text)
        self.assertIn("Mode: prd_backed", prd_text)
        self.assertIn(f"Manifest: `.vico/index/{slug}.json`", prd_text)
        self.assertIn(f"Execution Plan: `.vico/plans/active/{slug}.md`", prd_text)

    def test_close_slug_deletes_active_docs_and_cleans(self) -> None:
        root = self.make_repo()
        date = "2026-04-08"
        slug = self.dated_slug(date, "done-work")
        run_ok(
            str(PLAN_BOOTSTRAP_SCRIPT),
            "done-work",
            "Done Work",
            "--repo-root",
            str(root),
            "--level",
            "prd_backed",
            "--date",
            date,
        )
        (root / ".vico" / "resume" / f"{slug}.md").write_text("## Resume Summary\n", encoding="utf-8")
        run_ok(str(INDEX_SCRIPT), slug, "--repo-root", str(root))
        run_ok(str(CLOSE_SCRIPT), slug, "--repo-root", str(root))

        self.assertFalse((root / ".vico" / "plans" / "active" / f"{slug}.md").exists())
        self.assertFalse((root / ".vico" / "prd" / "active" / f"{slug}.md").exists())
        self.assertFalse((root / ".vico" / "resume" / f"{slug}.md").exists())
        self.assertFalse((root / ".vico" / "index" / f"{slug}.json").exists())
        self.assertFalse((root / ".vico" / "plans" / "archive" / f"{slug}.md").exists())

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
        self.assertTrue(plan.exists())
        self.assertEqual(plan.read_text(encoding="utf-8"), before)

    def test_close_slug_requires_exact_active_slug(self) -> None:
        root = self.make_repo()
        date = "2026-04-09"
        slug = self.dated_slug(date, "exact-match")
        run_ok(
            str(PLAN_BOOTSTRAP_SCRIPT),
            "exact-match",
            "Exact Match",
            "--repo-root",
            str(root),
            "--date",
            date,
        )

        result = subprocess.run(
            [sys.executable, str(CLOSE_SCRIPT), "exact-match", "--repo-root", str(root)],
            text=True,
            capture_output=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("No active plan or PRD found", result.stderr)
        self.assertTrue((root / ".vico" / "plans" / "active" / f"{slug}.md").exists())

    def test_sync_headers_is_idempotent_without_touch_updated(self) -> None:
        root = self.make_repo()
        date = "2026-04-09"
        slug = self.dated_slug(date, "idempotent")
        run_ok(
            str(PLAN_BOOTSTRAP_SCRIPT),
            "idempotent",
            "Idempotent",
            "--repo-root",
            str(root),
            "--level",
            "prd_backed",
            "--date",
            date,
        )
        plan = root / ".vico" / "plans" / "active" / f"{slug}.md"
        before = plan.read_text(encoding="utf-8")

        result = run_ok(str(HEADERS_SCRIPT), slug, "--repo-root", str(root))
        self.assertIn(f"Up to date: {slug}", result.stdout)
        self.assertEqual(plan.read_text(encoding="utf-8"), before)

    def test_probe_default_routing_contract_and_help_are_aligned(self) -> None:
        probe_skill = self.read(PROBE_SKILL)
        probe_help = self.read(PROBE_HELP)
        readme = self.read(README)
        readme_zh = self.read(README_ZH)

        self.assertIn("## Default Routing Rules", probe_skill)
        self.assertIn("recommendation-grade", probe_skill)
        self.assertIn("ask-user", probe_skill)
        self.assertIn("Do not force `grill` as the default", probe_skill)

        self.assertIn("route by issue state instead of forcing questioning every time", probe_help)
        self.assertIn("do a light scan first, then route into recommendation, one question, review, grill, or resolve", probe_help)

        self.assertIn("recommends, asks one question, reviews, or resolves based on issue state", readme)
        self.assertIn("根据 issue state 决定是直接建议、发一问、进入 `review`，还是直接收口", readme_zh)

    def test_workflow_readme_and_help_templates_express_default_light_escalation_model(self) -> None:
        readme = self.read(README)
        readme_zh = self.read(README_ZH)
        probe_help = self.read(PROBE_HELP)
        plan_help = self.read(PLAN_HELP)
        exec_help = self.read(SKILLS_ROOT / "vico-exec" / "references" / "help-template.md")

        self.assertIn("Default Light, Escalate When Needed.", readme)
        self.assertIn("probing and execution are separate escalation axes", readme)
        self.assertIn("默认从轻，按需升级。", readme_zh)
        self.assertIn("probing 和 execution 是两条独立的升级轴", readme_zh)

        self.assertIn("Axis position: the probing axis", probe_help)
        self.assertIn("Axis position: the tracked-execution front door", plan_help)
        self.assertIn("Axis position: the heavy end of the execution axis", exec_help)

    def test_repo_docs_define_persistence_policy_and_common_paths(self) -> None:
        readme = self.read(README)
        readme_zh = self.read(README_ZH)
        contracts = self.read(SKILLS_ROOT / "CONTRACTS.md")
        contracts_zh = self.read(SKILLS_ROOT / "CONTRACTS-zh.md")

        self.assertIn("## Persistence Policy", readme)
        self.assertIn("## Most Common Paths", readme)
        self.assertIn("## Escalation Hints", readme)
        self.assertIn("## Route Shifts", readme)
        self.assertIn("## Natural Triggers", readme)
        self.assertIn("## Route Visibility", readme)
        self.assertIn("## Install And Uninstall", readme)
        self.assertIn("## Feedback Flow", readme)
        self.assertIn("`vico-probe grill plan -> vico-plan`", readme)
        self.assertIn("how do I use vico-probe", readme)
        self.assertIn("how do I use vico-plan", readme)
        self.assertIn("verify this plan", readme)
        self.assertIn("how do I use vico-exec", readme)
        self.assertIn("how do I use vico-feedback", readme)
        self.assertIn("auto-classify the report as `bug`, `ux_friction`, `contract_gap`, or `feature_request`", readme)
        self.assertIn("Let `vico-feedback` classify it and draft the issue.", readme)
        self.assertIn("`vico-probe`: keep probe state session-local by default", readme)
        self.assertIn("`vico-plan`: write or update active plan", readme)
        self.assertIn("`vico-exec`: persist plan, index, or temporary reconcile updates", readme)
        self.assertIn("use `vico-exec` only when an active plan already exists", readme)
        self.assertIn("If a natural-language request could reasonably mean more than one of these routes", readme)
        self.assertIn("Skill route: <skill-name>", readme)
        self.assertIn("Route reason: <natural trigger | explicit skill request>", readme)
        self.assertIn("direct_execute -> vico-plan", readme)
        self.assertIn("vico-plan -> direct_execute", readme)
        self.assertIn("vico-probe -> direct_execute", readme)
        self.assertIn("Recommended install path: use `npx skills@latest`.", readme)
        self.assertIn("### Install With `npx skills@latest`", readme)
        self.assertIn("### Uninstall With `npx skills@latest`", readme)
        self.assertIn("### Development Link", readme)
        self.assertIn("### Uninstall", readme)
        self.assertIn("--agent codex", readme)
        self.assertIn("--agent claude-code", readme)
        self.assertIn("Unix-like systems: use `ln -s`", readme)
        self.assertIn("Vercel Skills docs:", readme)
        self.assertIn("Vercel skills guide:", readme)

        self.assertIn("## 落盘原则", readme_zh)
        self.assertIn("## 最常用路径", readme_zh)
        self.assertIn("## 升级提示", readme_zh)
        self.assertIn("## Route Shifts", readme_zh)
        self.assertIn("## 自然触发词", readme_zh)
        self.assertIn("## 路由可见性", readme_zh)
        self.assertIn("## 安装与卸载", readme_zh)
        self.assertIn("## 反馈流程", readme_zh)
        self.assertIn("`vico-probe grill plan -> vico-plan`", readme_zh)
        self.assertIn("vico-probe 如何使用", readme_zh)
        self.assertIn("vico-plan 如何使用", readme_zh)
        self.assertIn("verify this plan", readme_zh)
        self.assertIn("vico-exec 如何使用", readme_zh)
        self.assertIn("vico-feedback 如何使用", readme_zh)
        self.assertIn("默认应根据用户表达和上下文自动归类为 `bug`、`ux_friction`、`contract_gap` 或 `feature_request`", readme_zh)
        self.assertIn("让 `vico-feedback` 自动归类并生成 issue 草稿。", readme_zh)
        self.assertIn("优先用一句简短确认来消歧", readme_zh)
        self.assertIn("Skill route: <skill-name>", readme_zh)
        self.assertIn("Route reason: <natural trigger | explicit skill request>", readme_zh)
        self.assertIn("direct_execute -> vico-plan", readme_zh)
        self.assertIn("vico-plan -> direct_execute", readme_zh)
        self.assertIn("vico-probe -> direct_execute", readme_zh)
        self.assertIn("推荐安装方式：使用 `npx skills@latest`。", readme_zh)
        self.assertIn("### 用 `npx skills@latest` 安装", readme_zh)
        self.assertIn("### 开发期 Link", readme_zh)
        self.assertIn("### 卸载", readme_zh)
        self.assertIn("--agent codex", readme_zh)
        self.assertIn("--agent claude-code", readme_zh)
        self.assertIn("Unix-like 系统：使用 `ln -s`", readme_zh)
        self.assertIn("Vercel Skills 文档：", readme_zh)
        self.assertIn("Vercel skills 使用指南：", readme_zh)
        self.assertIn("## Persistence Policy", contracts)
        self.assertIn("## User-Facing Vs Internal", contracts)
        self.assertIn("`direct_execute`", contracts)
        self.assertIn("`vico-plan -> vico-exec`", contracts)
        self.assertIn("## Route Shift Policy", contracts)
        self.assertIn("Workflow re-entry is a first-class supported path", contracts)
        self.assertIn("## Verification Authority", contracts)
        self.assertIn("## Public Modes Vs Status Values", contracts)
        self.assertIn("## External Side Effects", contracts)
        self.assertIn("## 落盘原则", contracts_zh)
        self.assertIn("## 面向用户 vs 内部状态", contracts_zh)
        self.assertIn("`direct_execute`", contracts_zh)
        self.assertIn("`vico-plan -> vico-exec`", contracts_zh)
        self.assertIn("## Route Shift 策略", contracts_zh)
        self.assertIn("workflow re-entry 是一等支持路径", contracts_zh)
        self.assertIn("## 核验权威性", contracts_zh)
        self.assertIn("## 公开模式名 vs 状态值", contracts_zh)
        self.assertIn("## 外部副作用", contracts_zh)

    def test_probe_handoff_strong_inputs_align_between_probe_and_plan(self) -> None:
        probe_skill = self.read(PROBE_SKILL)
        plan_skill = self.read(PLAN_SKILL)
        handoff_template = self.read(PROBE_HANDOFF_TEMPLATE)

        for required in (
            "`Target`",
            "optional `Slug`",
            "optional `Issue classes`",
            "`Accepted decisions`",
            "`Unresolved decisions`",
            "`Suggested edits`",
        ):
            self.assertIn(required, probe_skill)
            self.assertIn(required, plan_skill)

        self.assertIn("- Optional: Slug", handoff_template)
        self.assertIn("- Optional: Issue classes", handoff_template)
        self.assertIn("- Optional: Recommended tracking mode", handoff_template)
        self.assertIn("- Optional: Suggested first slice", handoff_template)
        self.assertIn("- Optional: Execution readiness risks", handoff_template)
        self.assertIn("- Optional: Resolved during probe", handoff_template)
        self.assertIn("`vico-plan` should treat these as strong inputs", handoff_template)

    def test_plan_contract_defines_execution_readiness_and_probe_consumption_hints(self) -> None:
        plan_skill = self.read(PLAN_SKILL)
        handoff_template = self.read(PROBE_HANDOFF_TEMPLATE)
        plan_template = self.read(SKILLS_ROOT / "vico-plan" / "references" / "templates" / "plan-template.md")
        plan_only_template = self.read(SKILLS_ROOT / "vico-plan" / "references" / "templates" / "plan-only-template.md")

        self.assertIn("## Execution Readiness Rules", plan_skill)
        self.assertIn("## Verification Rules", plan_skill)
        self.assertIn("Recommended tracking mode", plan_skill)
        self.assertIn("Suggested first slice", plan_skill)
        self.assertIn("Execution readiness risks", plan_skill)
        self.assertIn("Resolved during probe", plan_skill)
        self.assertIn("make a plan", plan_skill)
        self.assertIn("verify this plan", plan_skill)
        self.assertIn("`verify close`", plan_skill)
        self.assertIn("`verify sync`", plan_skill)
        self.assertIn("`verify replan`", plan_skill)
        self.assertIn("how do I use vico-plan", plan_skill)
        self.assertIn("If the user's intent could reasonably map to lightweight direct execution instead of tracked planning", plan_skill)
        self.assertIn("keep internal routing and reconciliation heuristics implicit by default", plan_skill)
        self.assertIn("When work re-enters tracked planning after direct execution", plan_skill)
        self.assertIn("Treat that re-entry behavior as first-class", plan_skill)
        self.assertIn("A plan is `vico-exec` ready only when the next smallest unblocked slice can be chosen without guessing", plan_skill)
        self.assertIn("If the current plan is too coarse, too stale, or too ambiguous", plan_skill)

        self.assertIn("Optional: Recommended tracking mode", handoff_template)
        self.assertIn("Optional: Suggested first slice", handoff_template)
        self.assertIn("Optional: Execution readiness risks", handoff_template)
        self.assertIn("Optional: Resolved during probe", handoff_template)
        self.assertIn("A plan is `vico-exec` ready only when the next slice can be chosen without guessing", plan_template)
        self.assertIn("A plan is `vico-exec` ready only when the next slice can be chosen without guessing", plan_only_template)
        plan_verify = self.read(PLAN_VERIFY)
        self.assertIn("## Plan Verify", plan_verify)
        self.assertIn("`verified_complete` | `not_complete` | `ambiguous`", plan_verify)
        self.assertIn("## Evidence", plan_verify)
        self.assertIn("## Open Gaps", plan_verify)
        self.assertIn("## Recommended Action", plan_verify)
        self.assertIn("`direct_execute`", plan_verify)
        self.assertIn("`vico-plan -> vico-exec`", plan_verify)
        self.assertIn("## Recommended Next Mode", plan_verify)
        self.assertIn("`verify close`", plan_verify)
        self.assertIn("`verify sync`", plan_verify)
        self.assertIn("`verify replan`", plan_verify)
        self.assertIn("`verify` must be read-only", plan_verify)

    def test_plan_public_modes_drop_reset_and_keep_replan(self) -> None:
        plan_skill = self.read(PLAN_SKILL)
        plan_help = self.read(PLAN_HELP)

        self.assertIn("`replan`", plan_skill)
        self.assertIn("`verify`", plan_skill)
        self.assertIn("- replan", plan_help)
        self.assertIn("- verify", plan_help)
        self.assertIn("`verify close`: use when you want verification to gate an immediate close-out", plan_help)
        self.assertIn("`verify sync`: use when you want verification to gate an immediate state refresh", plan_help)
        self.assertIn("`verify replan`: use when you want verification to gate an immediate execution-contract rewrite", plan_help)
        self.assertIn("Use `replan` as the single public mode for same-slug execution-contract rewrites.", plan_skill)
        self.assertNotIn("- `reset`", plan_skill)
        self.assertNotIn("- reset", plan_help)

    def test_probe_examples_cover_all_modes_and_drop_stale_contract_examples(self) -> None:
        probe_help = self.read(PROBE_HELP)
        probe_output = self.read(PROBE_OUTPUT)

        for example in (
            "`vico-probe scan`",
            "`vico-probe grill`",
            "`vico-probe review`",
            "`vico-probe resolve`",
        ):
            self.assertIn(example, probe_help)

        for section in (
            "## Scan Example",
            "## Review Example",
            "## Grill Example",
            "## Probe Handoff Example",
        ):
            self.assertIn(section, probe_output)

        self.assertNotIn("review` and `resolve` are not formal modes yet", probe_output)
        self.assertNotIn("handoff template lacks `Target`", probe_output)
        self.assertIn("Issue classes", probe_output)
        self.assertIn("Findings", probe_output)
        self.assertIn("[critical] Controller-driven default:", probe_output)
        self.assertIn("Recommended action", probe_output)
        self.assertIn("Suggested next target", probe_output)
        self.assertIn("This probe is ready to hand to `vico-plan`.", probe_output)

    def test_probe_mode_set_is_consistent_across_skill_help_and_readme(self) -> None:
        probe_skill = self.read(PROBE_SKILL)
        probe_help = self.read(PROBE_HELP)
        readme = self.read(README)
        readme_zh = self.read(README_ZH)

        expected_modes = (
            "`scan`",
            "`grill`",
            "`review`",
            "`resolve`",
            "`help`",
        )
        for mode in expected_modes:
            self.assertIn(mode, probe_skill)

        for command in (
            "`vico-probe scan`",
            "`vico-probe grill`",
            "`vico-probe review`",
            "`vico-probe resolve`",
            "`vico-probe help`",
        ):
            self.assertIn(command, probe_help)
            self.assertIn(command, readme)
            self.assertIn(command, readme_zh)

    def test_probe_topic_map_controls_and_agent_default_mode_are_consistent(self) -> None:
        probe_skill = self.read(PROBE_SKILL)
        probe_help = self.read(PROBE_HELP)
        probe_agent = self.read(SKILLS_ROOT / "vico-probe" / "agents" / "openai.yaml")

        for control in (
            "`show`",
            "`add`",
            "`delete`",
            "`split`",
            "`merge`",
            "`retire`",
            "`reprioritize`",
        ):
            self.assertIn(control, probe_skill)

        for control in (
            "- show",
            "- add",
            "- delete",
            "- split",
            "- merge",
            "- retire",
            "- reprioritize",
        ):
            self.assertIn(control, probe_help)

        self.assertIn("default to concise mode unless the user asks for detailed mode", probe_agent)
        self.assertNotIn("use the detailed contract in SKILL.md", probe_agent)

    def test_probe_textual_outputs_follow_user_language_while_preserving_stable_literals(self) -> None:
        probe_skill = self.read(PROBE_SKILL)
        probe_help = self.read(PROBE_HELP)

        self.assertIn("user's primary working language", probe_skill)
        self.assertIn("most recent substantive message", probe_skill)
        self.assertIn("machine-consumed `Probe Handoff` field names stable", probe_skill)
        self.assertIn("scan the repo", probe_skill)
        self.assertIn("how do I use vico-probe", probe_skill)
        self.assertIn("If the user's intent could reasonably map to `probe`, `plan`, or `exec`", probe_skill)

        self.assertIn("user's primary working language", probe_help)
        self.assertIn("Keep commands and mode literals unchanged.", probe_help)
        self.assertIn("surface `Skill route` and `Route reason` in the first visible update when `vico-probe` is selected", probe_help)
        self.assertIn("## Grill Shortcuts", probe_help)
        self.assertIn("## Plan Targets", probe_help)
        self.assertIn("`grill plan`: grill the current active plan as the target object", probe_help)
        self.assertIn("`推` / `rec`: choose the recommended option", probe_help)
        self.assertIn("`做` / `do`: apply immediately", probe_help)

    def test_probe_explicit_submodes_bootstrap_scan_when_probe_state_is_missing(self) -> None:
        probe_skill = self.read(PROBE_SKILL)
        probe_help = self.read(PROBE_HELP)

        self.assertIn("explicit submode is invoked without a usable current issue bank", probe_skill)
        self.assertIn("perform a lightweight bootstrap scan first", probe_skill)
        self.assertIn("`resolve` does not require a prior `grill` pass", probe_skill)
        self.assertIn(
            "if major `ask-user` issues still remain after bootstrap triage, keep them in `Unresolved decisions` and `Recommended resolutions` rather than opening a new question during `resolve`",
            probe_skill,
        )

        self.assertIn(
            "bootstrap a light scan when explicit `grill`, `review`, or `resolve` is invoked without usable current probe state",
            probe_help,
        )
        self.assertIn("if a bounded, low-risk issue becomes immediately solvable during `grill`", probe_skill)
        self.assertIn("briefly solve it, refresh the evidence and issue state, and then continue `grill`", probe_skill)
        self.assertIn("allow a brief solve-and-return inside `grill` for bounded low-risk issues", probe_help)
        self.assertIn("`推` or `rec` = choose the recommended option", probe_skill)
        self.assertIn("`做` or `do` = apply immediately", probe_skill)
        self.assertIn("`留` or `hold` = decide now but do not apply immediately", probe_skill)
        self.assertIn("`继续` or `cont` = continue `grill`", probe_skill)
        self.assertIn("`收口` or `close` = stop questioning after this answer", probe_skill)
        self.assertIn("if an issue is solved during `grill`, mark it `decided`", probe_skill)
        self.assertIn("Resolved during probe", probe_skill)
        self.assertIn("umbrella verb for inspect + ask + targeted refinement", probe_skill)
        self.assertIn("If the target object is an active plan", probe_skill)
        self.assertIn("Only expose full issue-bank style detail when the user asks for it", probe_skill)
        self.assertIn("`- [priority] Title: explanation`", probe_skill)
        self.assertIn("If the next clear consumer is `vico-plan`, emit a self-contained `## Probe Handoff` block", probe_skill)
        self.assertIn("Do not use `see above` or other relative references inside a `Probe Handoff`", probe_skill)
        self.assertIn("`direct_execute`", probe_skill)
        self.assertIn("`vico-plan -> vico-exec`", probe_skill)
        self.assertIn("`scan` may legitimately suggest another narrower `scan`", probe_skill)
        self.assertIn("controlled recursive narrowing process", probe_skill)
        self.assertIn("Suggested next target", probe_skill)
        self.assertIn("accept short action modifiers in `grill`", probe_help)
        self.assertIn("`Findings`", probe_skill)
        self.assertIn("default `scan` output should emphasize user-facing findings over raw triage state", probe_skill)

    def test_probe_priority_rubric_covers_enforcement_boundaries_and_folded_scan_items(self) -> None:
        probe_skill = self.read(PROBE_SKILL)
        probe_output = self.read(PROBE_OUTPUT)

        self.assertIn("validator hard-fail behavior", probe_skill)
        self.assertIn("system-wide contract boundary or enforcement boundary", probe_skill)
        self.assertIn("system-wide enforcement boundary or distribution/runtime contract", probe_skill)
        self.assertIn("low-risk aliases", probe_skill)
        self.assertIn("folded `scan` items", probe_skill)
        self.assertIn("validator hard-fail rules still change the install model", probe_output)
        self.assertIn("Accepted short replies", probe_output)
        self.assertIn("`1 do cont`", probe_output)
        self.assertIn("`rec do`", probe_output)

    def test_probe_tree_has_no_legacy_grill_branding(self) -> None:
        probe_skill = self.read(PROBE_SKILL)
        probe_help = self.read(PROBE_HELP)
        probe_output = self.read(PROBE_OUTPUT)

        for text in (probe_skill, probe_help, probe_output):
            self.assertNotIn("vico-grill", text)
            self.assertNotIn("Grill Handoff", text)

        self.assertIn("# Vico Probe Output Format", probe_output)

    def test_probe_contract_no_longer_supports_batch_mode(self) -> None:
        probe_skill = self.read(PROBE_SKILL)
        probe_help = self.read(PROBE_HELP)
        probe_output = self.read(PROBE_OUTPUT)

        self.assertNotIn("## Batch Question Mode", probe_skill)
        self.assertNotIn("Batch N", probe_skill)
        self.assertNotIn("Batch rationale", probe_skill)
        self.assertNotIn("small batch", probe_help)
        self.assertNotIn("## Batch Question Example", probe_output)
        self.assertNotIn("Batch 9", probe_output)

    def test_plan_textual_outputs_follow_user_language_while_preserving_stable_literals(self) -> None:
        plan_skill = self.read(PLAN_SKILL)
        plan_help = self.read(PLAN_HELP)
        plan_review = self.read(PLAN_REVIEW)
        plan_truth = self.read(PLAN_TRUTH)

        self.assertIn("user's primary working language", plan_skill)
        self.assertIn("most recent substantive message", plan_skill)
        self.assertIn("machine-consumed handoff field names stable", plan_skill)

        self.assertIn("user's primary working language", plan_help)
        self.assertIn("Keep commands and mode literals unchanged.", plan_help)
        self.assertIn("## Route Visibility", plan_help)
        self.assertIn("show `Skill route` and `Route reason` in the first visible update when `vico-plan` is selected", plan_help)
        self.assertIn("## Mode Hints", plan_help)
        self.assertIn("`verify`: use when you need to check completion against real code and test evidence before close-out", plan_help)
        self.assertIn("`sync`: use when code moved and the current plan should catch up", plan_help)
        self.assertIn("`replan`: use when the same slug still applies", plan_help)
        self.assertIn("`prd`: use when the work now needs or updates `prd_backed` framing", plan_help)

        self.assertIn("user's primary working language", plan_review)
        self.assertIn("Keep commands, mode literals, status literals, and slug/path literals unchanged.", plan_review)

        plan_verify = self.read(PLAN_VERIFY)
        self.assertIn("## Plan Verify", plan_verify)
        self.assertIn("`verified_complete` | `not_complete` | `ambiguous`", plan_verify)
        self.assertIn("## Evidence", plan_verify)
        self.assertIn("## Open Gaps", plan_verify)
        self.assertIn("## Recommended Next Mode", plan_verify)
        self.assertIn("`verify` must be read-only", plan_verify)

        self.assertIn("user's primary working language", plan_truth)
        self.assertIn("Keep commands, path literals, and stable field labels unchanged when another workflow consumes them.", plan_truth)

    def test_exec_help_template_has_language_rule_and_axis_position(self) -> None:
        exec_help = self.read(EXEC_HELP)

        self.assertIn("user's primary working language", exec_help)
        self.assertIn("Keep commands and mode literals unchanged.", exec_help)
        self.assertIn("show `Skill route` and `Route reason` in the first visible update when `vico-exec` is selected", exec_help)
        self.assertIn("Axis position: the heavy end of the execution axis", exec_help)
        self.assertIn("do not guess the execution target when multiple active slugs are plausible", exec_help)

    def test_exec_output_contract_covers_language_and_persistence(self) -> None:
        exec_skill = self.read(EXEC_SKILL)
        exec_report = self.read(SKILLS_ROOT / "vico-exec" / "references" / "execution-report-template.md")
        blocker_taxonomy = self.read(SKILLS_ROOT / "vico-exec" / "references" / "blocker-taxonomy.md")

        self.assertIn("## Output Contract", exec_skill)
        self.assertIn("keep going", exec_skill)
        self.assertIn("how do I use vico-exec", exec_skill)
        self.assertIn("If the user sounds like they want persistent execution but no active plan exists", exec_skill)
        self.assertIn("Treat direct-execution detours as normal", exec_skill)
        self.assertIn("user's primary working language", exec_skill)
        self.assertIn("most recent substantive message", exec_skill)
        self.assertIn("keep commands, status literals, blocker types, file paths", exec_skill)
        self.assertIn("persist plan, index, or temporary reconcile updates to disk", exec_skill)
        self.assertIn("do not fabricate disk writes when no execution-state change is needed", exec_skill)
        self.assertIn("Persist execution-state changes to disk when they are needed to preserve continuity across turns or tools.", exec_skill)
        self.assertIn("## Multi-Active Safety Rules", exec_skill)
        self.assertIn("do not guess. Ask for an explicit slug or route back through `vico-plan review`", exec_skill)
        self.assertIn("include the active source, active slug, and continuation basis in the execution report", exec_skill)
        self.assertIn("keep deeper continuation heuristics implicit by default", exec_skill)

        self.assertIn("user's primary working language", exec_report)
        self.assertIn("Keep commands, status literals, blocker types, and path literals unchanged.", exec_report)
        self.assertIn("## Execution State", exec_report)
        self.assertIn("blocked output shape", exec_skill)
        self.assertIn("## Blocked Output Shape", blocker_taxonomy)
        self.assertIn("## Blocked", blocker_taxonomy)
        self.assertIn("- Type:", blocker_taxonomy)
        self.assertIn("- Evidence:", blocker_taxonomy)
        self.assertIn("- Unblock:", blocker_taxonomy)
        self.assertIn("- Next step:", blocker_taxonomy)

    def test_exec_runtime_closure_uses_local_references_and_scripts(self) -> None:
        exec_skill = self.read(EXEC_SKILL)
        exec_automation = self.read(EXEC_AUTOMATION)
        exec_status = self.read(EXEC_STATUS)
        exec_sync_script = self.read(EXEC_SYNC_SCRIPT)

        self.assertIn("Prefer `scripts/sync_vico_index.py`", exec_skill)
        self.assertIn("Use [references/status-vocabulary.md]", exec_skill)
        self.assertIn("Use [references/automation.md]", exec_skill)
        self.assertNotIn("../vico-plan/", exec_skill)

        self.assertIn("Use `scripts/sync_vico_index.py`", exec_automation)
        self.assertNotIn("../vico-plan/", exec_automation)
        self.assertIn("## Execution Progress", exec_status)
        self.assertIn("from vico_common import", exec_sync_script)

    def test_feedback_skill_is_present_and_issue_draft_oriented(self) -> None:
        feedback_skill = self.read(FEEDBACK_SKILL)
        feedback_help = self.read(FEEDBACK_HELP)
        feedback_issue = self.read(FEEDBACK_ISSUE)

        self.assertIn("GitHub issue draft", feedback_skill)
        self.assertIn("bug", feedback_skill)
        self.assertIn("ux_friction", feedback_skill)
        self.assertIn("contract_gap", feedback_skill)
        self.assertIn("feature_request", feedback_skill)
        self.assertIn("gh issue create", feedback_skill)
        self.assertIn("gh issue comment", feedback_skill)
        self.assertIn("only create the issue after explicit user confirmation", feedback_skill)
        self.assertIn("Default to automatic classification", feedback_skill)
        self.assertIn("how do I use vico-feedback", feedback_skill)
        self.assertIn("reopen the matching issue with `gh issue reopen`", feedback_skill)

        self.assertIn("## Vico Feedback Help", feedback_help)
        self.assertIn("GitHub issue draft", feedback_help)
        self.assertIn("classify the feedback automatically", feedback_help)
        self.assertIn("suggest `create`, `reopen`, or `comment`", feedback_help)
        self.assertIn("surface `Skill route` and `Route reason`", feedback_help)

        self.assertIn("Title", feedback_issue)
        self.assertIn("Type", feedback_issue)
        self.assertIn("Affected skills", feedback_issue)
        self.assertIn("Current behavior", feedback_issue)
        self.assertIn("Expected behavior", feedback_issue)
        self.assertIn("Why it matters", feedback_issue)
        self.assertIn("Recommended issue action", feedback_issue)


if __name__ == "__main__":
    unittest.main()
