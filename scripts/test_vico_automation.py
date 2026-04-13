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
GROUND_EXPORT_MD_SCRIPT = SKILLS_ROOT / "vico-ground" / "scripts" / "export_vico_operating_md.py"

GROUND_SKILL = SKILLS_ROOT / "vico-ground" / "SKILL.md"
GROUND_HELP = SKILLS_ROOT / "vico-ground" / "references" / "help-template.md"
GROUND_OUTPUT = SKILLS_ROOT / "vico-ground" / "references" / "output-format.md"
PLAN_SKILL = SKILLS_ROOT / "vico-plan" / "SKILL.md"
PLAN_HELP = SKILLS_ROOT / "vico-plan" / "references" / "templates" / "help-template.md"
PLAN_REVIEW = SKILLS_ROOT / "vico-plan" / "references" / "templates" / "review-template.md"
PLAN_VERIFY = SKILLS_ROOT / "vico-plan" / "references" / "templates" / "verify-template.md"
PLAN_TRUTH = SKILLS_ROOT / "vico-plan" / "references" / "templates" / "truth-template.md"
GROUND_HANDOFF_TEMPLATE = SKILLS_ROOT / "vico-plan" / "references" / "templates" / "ground-handoff-template.md"
EXEC_SKILL = SKILLS_ROOT / "vico-exec" / "SKILL.md"
EXEC_HELP = SKILLS_ROOT / "vico-exec" / "references" / "help-template.md"
EXEC_AUTOMATION = SKILLS_ROOT / "vico-exec" / "references" / "automation.md"
EXEC_RUNNER = SKILLS_ROOT / "vico-exec" / "scripts" / "claude_exec_runner.py"
EXEC_RUNNER_REF = SKILLS_ROOT / "vico-exec" / "references" / "runner.md"
EXEC_CC_OPERATOR = SKILLS_ROOT / "vico-exec" / "references" / "cc-operator.md"
FEEDBACK_SKILL = SKILLS_ROOT / "vico-feedback" / "SKILL.md"
FEEDBACK_HELP = SKILLS_ROOT / "vico-feedback" / "references" / "help-template.md"
README = SKILLS_ROOT / "README.md"
README_ZH = SKILLS_ROOT / "README-zh.md"
CONSENSUS = SKILLS_ROOT / "CONSENSUS.md"
CONSENSUS_ZH = SKILLS_ROOT / "CONSENSUS-zh.md"


def run_ok(*args: str) -> subprocess.CompletedProcess[str]:
    result = subprocess.run([sys.executable, *args], text=True, capture_output=True)
    if result.returncode != 0:
        raise AssertionError(f"Command failed: {' '.join(args)}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}")
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
        run_ok(str(PLAN_BOOTSTRAP_SCRIPT), "tiny-fix", "Tiny Fix", "--repo-root", str(root), "--date", date)

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

        plan_text = (root / ".vico" / "plans" / "active" / f"{slug}.md").read_text(encoding="utf-8")
        self.assertIn(f"> Manifest: `.vico/index/{slug}.json`", plan_text)

    def test_close_slug_dry_run_surfaces_reason_and_does_not_mutate_files(self) -> None:
        root = self.make_repo()
        date = "2026-04-09"
        slug = self.dated_slug(date, "cancel-me")
        run_ok(str(PLAN_BOOTSTRAP_SCRIPT), "cancel-me", "Cancel Me", "--repo-root", str(root), "--date", date)

        plan = root / ".vico" / "plans" / "active" / f"{slug}.md"
        before = plan.read_text(encoding="utf-8")
        result = run_ok(str(CLOSE_SCRIPT), slug, "--repo-root", str(root), "--reason", "cancel", "--dry-run")
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
        run_ok(str(PLAN_BOOTSTRAP_SCRIPT), "export-me", "Export Me", "--repo-root", str(root), "--date", date)
        run_ok(str(GROUND_EXPORT_MD_SCRIPT), "AGENTS.md", "--repo-root", str(root))
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
        self.assertIn("problem framing and execution structure are separate escalation axes", readme)
        self.assertIn("### Escalation Map", readme)
        self.assertIn("Horizontal axis: problem-framing rigor", readme)
        self.assertIn("Vertical axis: execution structure", readme)
        self.assertIn("Codex: vico-plan -> Claude Code: vico-exec", readme)
        self.assertIn("vico-ground export-md AGENTS.md", readme)
        self.assertIn("Consensus guide: [CONSENSUS.md](CONSENSUS.md)", readme)
        self.assertIn("forrestchang/andrej-karpathy-skills", readme)
        self.assertIn("## Start Here", readme)
        self.assertIn("Three common paths", readme)

        self.assertIn("`vico-ground`", readme_zh)
        self.assertIn("问题澄清强度和执行结构强度是两条独立的升级轴", readme_zh)
        self.assertIn("### 升级坐标图", readme_zh)
        self.assertIn("Codex: vico-plan -> Claude Code: vico-exec", readme_zh)
        self.assertIn("vico-ground export-md AGENTS.md", readme_zh)
        self.assertIn("共识模型参考: [CONSENSUS-zh.md](CONSENSUS-zh.md)", readme_zh)
        self.assertIn("## 从这里开始", readme_zh)
        self.assertIn("三条最常见路径", readme_zh)

    def test_ground_skill_has_shared_ground_model_and_moves(self) -> None:
        ground_skill = self.read(GROUND_SKILL)
        ground_help = self.read(GROUND_HELP)
        ground_output = self.read(GROUND_OUTPUT)

        self.assertIn("shared-ground construction workflow", ground_skill)
        self.assertIn("## Theory Basis", ground_skill)
        self.assertIn("common ground", ground_skill)
        self.assertIn("conversational grounding", ground_skill)
        self.assertIn("## Grounding Principles", ground_skill)
        self.assertIn("## State Model", ground_skill)
        self.assertIn("Accepted Facts", ground_skill)
        self.assertIn("Active Assumptions", ground_skill)
        self.assertIn("Interpretations", ground_skill)
        self.assertIn("Findings", ground_skill)
        self.assertIn("Preferences", ground_skill)
        self.assertIn("Issue Bank", ground_skill)
        self.assertIn("Tradeoffs", ground_skill)
        self.assertIn("Commitments", ground_skill)
        self.assertIn("Ground Handoff", ground_skill)
        self.assertIn("Do not treat every `Finding` as an `Issue`", ground_skill)
        self.assertIn("## Epistemic Status Model", ground_skill)
        self.assertIn("`fact`", ground_skill)
        self.assertIn("`assumption`", ground_skill)
        self.assertIn("`interpretation`", ground_skill)
        self.assertIn("`preference`", ground_skill)
        self.assertIn("`commitment`", ground_skill)
        self.assertIn("## Epistemic Transition Rules", ground_skill)
        self.assertIn("`assumption -> fact`", ground_skill)
        self.assertIn("`preference -> commitment`", ground_skill)
        self.assertIn("## Moves", ground_skill)
        self.assertIn("`clarify`", ground_skill)
        self.assertIn("`scan`", ground_skill)
        self.assertIn("`map`", ground_skill)
        self.assertIn("`align`", ground_skill)
        self.assertIn("`reframe`", ground_skill)
        self.assertIn("`tradeoff`", ground_skill)
        self.assertIn("`grill`", ground_skill)
        self.assertIn("`challenge`", ground_skill)
        self.assertIn("`export-md`", ground_skill)
        self.assertIn("`review`", ground_skill)
        self.assertIn("`resolve`", ground_skill)
        self.assertIn("what is the highest-value missing condition for actionable shared ground?", ground_skill)
        self.assertIn("## Move Selection Rubric", ground_skill)
        self.assertIn("is the highest-value missing condition about intent or scope", ground_skill)
        self.assertIn("is the current ground already actionable and ready to hand forward", ground_skill)
        self.assertIn("ambiguity_reduction", ground_skill)
        self.assertIn("verification_impact", ground_skill)

        self.assertIn("## Vico Ground Help", ground_help)
        self.assertIn("- clarify", ground_help)
        self.assertIn("- reframe", ground_help)
        self.assertIn("- tradeoff", ground_help)
        self.assertIn("- grill", ground_help)
        self.assertIn("- challenge", ground_help)
        self.assertIn("- export-md", ground_help)
        self.assertIn("keep findings and issues separate", ground_help)

        self.assertIn("# Vico Ground Output Format", ground_output)
        self.assertIn("## Scan Example", ground_output)
        self.assertIn("## Ground Handoff Example", ground_output)
        self.assertIn("Findings", ground_output)
        self.assertIn("Preferences", ground_output)
        self.assertIn("Commitments", ground_output)
        self.assertIn("Invalidation triggers", ground_output)

    def test_plan_skill_consumes_ground_handoff_and_export_mode(self) -> None:
        plan_skill = self.read(PLAN_SKILL)
        plan_help = self.read(PLAN_HELP)
        handoff_template = self.read(GROUND_HANDOFF_TEMPLATE)

        self.assertIn("`vico-ground` handoff", plan_skill)
        self.assertIn("Treat a ground handoff as matching only when", plan_skill)
        self.assertIn("## Simplicity Discipline", plan_skill)

        self.assertIn("# Ground Handoff Template", handoff_template)
        self.assertIn("## Ground Handoff", handoff_template)
        self.assertIn("Optional: Active assumptions", handoff_template)
        self.assertIn("Optional: Preferences", handoff_template)
        self.assertIn("Optional: Tradeoffs", handoff_template)
        self.assertIn("Optional: Commitments", handoff_template)
        self.assertIn("Optional: Invalidation triggers", handoff_template)
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
        self.assertIn("`done` requires both implementation evidence and verification evidence.", exec_skill)

        self.assertIn("## Modes", exec_help)
        self.assertIn("- cc", exec_help)
        self.assertIn("vico-exec cc", exec_help)
        self.assertIn("run this with cc", exec_help)
        self.assertIn("handoff to cc", exec_help)

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

    def test_feedback_skill_is_present(self) -> None:
        feedback_skill = self.read(FEEDBACK_SKILL)
        feedback_help = self.read(FEEDBACK_HELP)
        self.assertIn("GitHub issue draft", feedback_skill)
        self.assertIn("how do I use vico-feedback", feedback_skill)
        self.assertIn("## Vico Feedback Help", feedback_help)

    def test_consensus_docs_exist_and_cover_major_theories(self) -> None:
        consensus = self.read(CONSENSUS)
        consensus_zh = self.read(CONSENSUS_ZH)

        self.assertIn("# Consensus Models", consensus)
        self.assertIn("### Common Ground", consensus)
        self.assertIn("### Conversational Grounding", consensus)
        self.assertIn("### Sensemaking", consensus)
        self.assertIn("### Deliberation And Argumentation", consensus)
        self.assertIn("### Negotiation And Preference Reconciliation", consensus)
        self.assertIn("### Vocabulary And Ontology Alignment", consensus)
        self.assertIn("## Practical Consensus Moves", consensus)
        self.assertIn("## Theory To Move Mapping", consensus)
        self.assertIn("| Theory family | Main failure it helps with | Best Vico moves | Typical grounded artifact |", consensus)
        self.assertIn("## Failure Patterns", consensus)
        self.assertIn("## Anti-Patterns", consensus)
        self.assertIn("clarify", consensus)
        self.assertIn("tradeoff", consensus)

        self.assertIn("# 共识模型", consensus_zh)
        self.assertIn("### Common Ground", consensus_zh)
        self.assertIn("### Conversational Grounding", consensus_zh)
        self.assertIn("### Sensemaking", consensus_zh)
        self.assertIn("## 可用的共识动作", consensus_zh)
        self.assertIn("## 理论到 Move 的映射表", consensus_zh)
        self.assertIn("## 失败模式", consensus_zh)
        self.assertIn("## 反模式", consensus_zh)


if __name__ == "__main__":
    unittest.main()
