#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

PLACEHOLDER_MARKERS = ("[TODO",)
MARKDOWN_LINK_RE = re.compile(r"\]\(([^)#\s]+)\)")
BACKTICK_PATH_RE = re.compile(r"`((?:\.\.?/|references/|scripts/|agents/)[^`\s]+)`")


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)


def find_skill_dirs(root: Path) -> list[Path]:
    return sorted(path for path in root.iterdir() if path.is_dir() and (path / "SKILL.md").exists())


def python_files_under(path: Path) -> list[Path]:
    if not path.exists():
        return []
    return sorted(file for file in path.rglob("*.py") if "__pycache__" not in file.parts)


def placeholder_hits(root: Path) -> list[str]:
    hits: list[str] = []
    for file in sorted(root.rglob("*")):
        if not file.is_file():
            continue
        if "__pycache__" in file.parts:
            continue
        if file.suffix.lower() not in {".md", ".yaml", ".yml", ".json", ".txt"}:
            continue
        text = file.read_text(encoding="utf-8")
        for line_number, line in enumerate(text.splitlines(), start=1):
            if any(marker in line for marker in PLACEHOLDER_MARKERS):
                hits.append(f"{file}:{line_number}:{line}")
    return hits


def pycache_dirs(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("__pycache__") if path.is_dir())


def remove_pycache_dirs(root: Path) -> None:
    for path in pycache_dirs(root):
        for child in sorted(path.rglob("*"), reverse=True):
            if child.is_file():
                child.unlink()
            elif child.is_dir():
                child.rmdir()
        path.rmdir()


def validate_wilco_probe_contract(root: Path) -> list[str]:
    failures: list[str] = []
    skill_path = root / "wilco-probe" / "SKILL.md"
    reference_path = root / "wilco-probe" / "references" / "output-format.md"
    agent_path = root / "wilco-probe" / "agents" / "openai.yaml"

    if not skill_path.exists():
        return [f"Missing wilco-probe skill file: {skill_path}"]
    if not reference_path.exists():
        failures.append(f"Missing wilco-probe output reference: {reference_path}")
    if not agent_path.exists():
        failures.append(f"Missing wilco-probe agent prompt: {agent_path}")

    skill_text = skill_path.read_text(encoding="utf-8")
    required_skill_markers = (
        "## Question Ordering Rules",
        "## Global Question Selection",
        "## Input Model",
        "## Internal State Model",
        "## Issue Classes",
        "## Topic Coverage States",
        "## Issue States",
        "## Topic Map Evolution",
        "## User Topic Map Controls",
        "## Topic Map Bootstrap Heuristics",
        "## Question Bank",
        "## Scoring Rubric",
        "## Topic Scheduling Rules",
        "## Output Contract",
        "### Concise Mode",
        "### Detailed Mode",
        "### Core Sections",
        "### Optional Sections",
        "## Priority Rubric",
        "## Stop Conditions",
        "## Summary Contract",
        "### Core Summary Sections",
        "### Optional Summary Sections",
        "If the next clear consumer is `wilco-plan`, emit a self-contained `## Probe Handoff` block",
        "Do not use `see above` or other relative references inside a `Probe Handoff`",
        "`direct_execute`",
        "`wilco-plan -> wilco-exec`",
        "## Anti-Patterns",
        "[references/output-format.md](references/output-format.md)",
        "`Question N: <question text>`",
        "`Accepted decisions`",
        "`Suggested edits`",
        "Mode: concise | available: concise, detailed",
        "Mode: detailed | available: concise, detailed",
        "dynamic working map",
        "## Recommendation Shortcut",
        "## Default Routing Rules",
        "### Scan Contract",
        "### Grill Contract",
        "### Review Contract",
        "### Resolve Contract",
        "explicit submode is invoked without a usable current issue bank",
        "perform a lightweight bootstrap scan first",
        "`resolve` does not require a prior `grill` pass",
        "if a bounded, low-risk issue becomes immediately solvable during `grill`",
        "briefly solve it, refresh the evidence and issue state, and then continue `grill`",
        "`推` or `rec` = choose the recommended option",
        "`做` or `do` = apply immediately",
        "`留` or `hold` = decide now but do not apply immediately",
        "`继续` or `cont` = continue `grill`",
        "`收口` or `close` = stop questioning after this answer",
        "if an issue is solved during `grill`, mark it `decided`",
        "Resolved during probe",
        "Intent Overlay",
        "Evidence Bank",
        "Issue Bank",
        "- `grill`",
        "- `review`",
        "- `resolve`",
        "Recommendation N:",
        "`add`",
        "`delete`",
        "`split`",
        "`merge`",
        "`retire`",
        "`reprioritize`",
        "portfolio-style selection",
        "highest-value next question",
        "impact",
        "dependency_unlock",
        "topic_saturation_penalty",
        "unvisited_topic_bonus",
        "Do not ask more than `2` consecutive questions from the same top-level topic",
        "user's primary working language",
        "most recent substantive message",
        "machine-consumed `Probe Handoff` field names stable",
        "umbrella verb for inspect + ask + targeted refinement",
        "If the target object is an active plan",
        "scan the repo",
        "how do I use wilco-probe",
        "If the user's intent could reasonably map to `probe`, `plan`, or `exec`",
        "validator hard-fail behavior",
        "system-wide contract boundary or enforcement boundary",
        "system-wide enforcement boundary or distribution/runtime contract",
        "low-risk aliases",
        "folded `scan` items",
        "`Findings`",
        "default `scan` output should emphasize user-facing findings over raw triage state",
        "Only expose full issue-bank style detail when the user asks for it",
        "`scan` may legitimately suggest another narrower `scan`",
        "controlled recursive narrowing process",
        "Suggested next target",
        "`- [priority] Title: explanation`",
    )
    for marker in required_skill_markers:
        if marker not in skill_text:
            failures.append(f"wilco-probe/SKILL.md missing marker: {marker}")

    if reference_path.exists():
        reference_text = reference_path.read_text(encoding="utf-8")
        required_reference_markers = (
            "## Concise Question Template",
            "## Cross-Topic Scheduling Example",
            "## Scan Example",
            "## Review Example",
            "## Grill Example",
            "## Object-Specific Topic Map Example",
            "## Candidate Ranking Example",
            "## Topic Coverage Example",
            "## Topic Map Snapshot Example",
            "## User-Directed Topic Map Update Example",
            "## Expanded Question Example",
            "## Final Summary Example",
            "Question 7:",
            "Recommendation 18:",
            "Target",
            "Issue classes",
            "Findings",
            "Evidence",
            "This probe is ready to hand to `wilco-plan`.",
            "Recommended action",
            "[critical] Controller-driven default:",
            "validator hard-fail rules still change the install model",
            "Accepted short replies",
            "`1 do cont`",
            "`rec do`",
            "Suggested next target",
            "Mode: concise | available: concise, detailed",
            "Mode: detailed | available: concise, detailed",
            "Accepted decisions",
        )
        for marker in required_reference_markers:
            if marker not in reference_text:
                failures.append(f"wilco-probe/references/output-format.md missing marker: {marker}")

    if agent_path.exists():
        agent_text = agent_path.read_text(encoding="utf-8")
        required_agent_markers = (
            "SKILL.md",
            "object-specific topic map",
            "top-level topic coverage state",
            "2 consecutive questions",
            "direct recommendation",
            "default to concise mode unless the user asks for detailed mode",
        )
        for marker in required_agent_markers:
            if marker not in agent_text:
                failures.append(f"wilco-probe/agents/openai.yaml missing marker: {marker}")
        if "use the detailed contract in SKILL.md" in agent_text:
            failures.append(
                "wilco-probe/agents/openai.yaml should not imply detailed mode is the default"
            )
        forbidden_agent_markers = (
            "Recommended answer",
            "Why it matters",
            "Decision dependency",
            "Write-back target",
        )
        for marker in forbidden_agent_markers:
            if marker in agent_text:
                failures.append(f"wilco-probe/agents/openai.yaml should not duplicate detailed contract marker: {marker}")

    user_controls_markers = ("`show`", "`add`", "`delete`", "`split`", "`merge`", "`retire`", "`reprioritize`")
    help_controls_markers = ("- show", "- add", "- delete", "- split", "- merge", "- retire", "- reprioritize")
    for marker in user_controls_markers:
        if marker not in skill_text:
            failures.append(f"wilco-probe/SKILL.md missing topic-map control: {marker}")
    if root.joinpath("wilco-probe", "references", "help-template.md").exists():
        help_text = root.joinpath("wilco-probe", "references", "help-template.md").read_text(encoding="utf-8")
        for marker in help_controls_markers:
            if marker not in help_text:
                failures.append(f"wilco-probe/references/help-template.md missing topic-map control: {marker}")
        for marker in (
            "## Grill Shortcuts",
            "`推` / `rec`: choose the recommended option",
            "`做` / `do`: apply immediately",
            "`留` / `hold`: decide now without applying",
            "`继续` / `cont`: continue `grill`",
            "`收口` / `close`: stop questioning and synthesize",
        ):
            if marker not in help_text:
                failures.append(f"wilco-probe/references/help-template.md missing grill shortcut marker: {marker}")

    return failures


def validate_wilco_exec_contract(root: Path) -> list[str]:
    failures: list[str] = []
    skill_path = root / "wilco-exec" / "SKILL.md"
    help_path = root / "wilco-exec" / "references" / "help-template.md"
    report_path = root / "wilco-exec" / "references" / "execution-report-template.md"
    agent_path = root / "wilco-exec" / "agents" / "openai.yaml"

    if not skill_path.exists():
        return [f"Missing wilco-exec skill file: {skill_path}"]
    if not help_path.exists():
        failures.append(f"Missing wilco-exec help template: {help_path}")
    if not report_path.exists():
        failures.append(f"Missing wilco-exec execution report template: {report_path}")
    if not agent_path.exists():
        failures.append(f"Missing wilco-exec agent prompt: {agent_path}")

    skill_text = skill_path.read_text(encoding="utf-8")
    required_skill_markers = (
        "## Mode Contract",
        "## Output Contract",
        "smallest unblocked next step",
        "route to `wilco-plan close` automatically",
        "keep going",
        "how do I use wilco-exec",
        "If the user sounds like they want persistent execution but no active plan exists",
        "user's primary working language",
        "most recent substantive message",
        "keep commands, status literals, blocker types, file paths",
        "persist plan, index, or temporary reconcile updates to disk",
        "do not fabricate disk writes when no execution-state change is needed",
        "Persist execution-state changes to disk when they are needed to preserve continuity across turns or tools.",
        "## Multi-Active Safety Rules",
        "do not guess. Ask for an explicit slug or route back through `wilco-plan review`",
        "include the active source, active slug, and continuation basis in the execution report",
        "keep deeper continuation heuristics implicit by default",
        "[references/execution-report-template.md](references/execution-report-template.md)",
    )
    for marker in required_skill_markers:
        if marker not in skill_text:
            failures.append(f"wilco-exec/SKILL.md missing marker: {marker}")

    if help_path.exists():
        help_text = help_path.read_text(encoding="utf-8")
        for marker in (
            "user's primary working language",
            "Keep commands and mode literals unchanged.",
            "Axis position: the heavy end of the execution axis",
            "do not guess the execution target when multiple active slugs are plausible",
        ):
            if marker not in help_text:
                failures.append(f"wilco-exec/references/help-template.md missing marker: {marker}")

    if report_path.exists():
        report_text = report_path.read_text(encoding="utf-8")
        for marker in (
            "user's primary working language",
            "Keep commands, status literals, blocker types, and path literals unchanged.",
            "## Execution Step",
            "## Execution State",
            "## Verification",
            "## Plan Update",
            "## Next Step",
        ):
            if marker not in report_text:
                failures.append(f"wilco-exec/references/execution-report-template.md missing marker: {marker}")

    if agent_path.exists():
        agent_text = agent_path.read_text(encoding="utf-8")
        for marker in (
            "active Wilco plan",
            "smallest unblocked next step",
            "verify it",
            "update the plan",
            "route to `wilco-plan close` automatically",
        ):
            if marker not in agent_text:
                failures.append(f"wilco-exec/agents/openai.yaml missing marker: {marker}")

    return failures


def validate_wilco_feedback_contract(root: Path) -> list[str]:
    failures: list[str] = []
    skill_path = root / "wilco-feedback" / "SKILL.md"
    help_path = root / "wilco-feedback" / "references" / "help-template.md"
    issue_path = root / "wilco-feedback" / "references" / "issue-template.md"
    agent_path = root / "wilco-feedback" / "agents" / "openai.yaml"

    if not skill_path.exists():
        return [f"Missing wilco-feedback skill file: {skill_path}"]
    for path, label in (
        (help_path, "help template"),
        (issue_path, "issue template"),
        (agent_path, "agent prompt"),
    ):
        if not path.exists():
            failures.append(f"Missing wilco-feedback {label}: {path}")

    skill_text = skill_path.read_text(encoding="utf-8")
    for marker in (
        "GitHub issue draft",
        "bug",
        "ux_friction",
        "contract_gap",
        "feature_request",
        "gh issue create",
        "only create the issue after explicit user confirmation",
        "Default to automatic classification",
        "reopen the matching issue with `gh issue reopen`",
        "gh issue comment",
        "Skill route",
        "Route reason",
        "how do I use wilco-feedback",
    ):
        if marker not in skill_text:
            failures.append(f"wilco-feedback/SKILL.md missing marker: {marker}")

    if help_path.exists():
        help_text = help_path.read_text(encoding="utf-8")
        for marker in (
            "## Wilco Feedback Help",
            "GitHub issue draft",
            "classify the feedback automatically",
            "suggest `create`, `reopen`, or `comment`",
            "surface `Skill route` and `Route reason`",
            "how do I use wilco-feedback",
        ):
            if marker not in help_text:
                failures.append(f"wilco-feedback/references/help-template.md missing marker: {marker}")

    if issue_path.exists():
        issue_text = issue_path.read_text(encoding="utf-8")
        for marker in (
            "Title",
            "Type",
            "Affected skills",
            "Current behavior",
            "Expected behavior",
            "Why it matters",
            "Recommended issue action",
        ):
            if marker not in issue_text:
                failures.append(f"wilco-feedback/references/issue-template.md missing marker: {marker}")

    if agent_path.exists():
        agent_text = agent_path.read_text(encoding="utf-8")
        for marker in (
            "GitHub issue draft",
            "only create the issue after explicit user confirmation",
        ):
            if marker not in agent_text:
                failures.append(f"wilco-feedback/agents/openai.yaml missing marker: {marker}")

    return failures


def validate_wilco_plan_contract(root: Path) -> list[str]:
    failures: list[str] = []
    skill_path = root / "wilco-plan" / "SKILL.md"
    help_path = root / "wilco-plan" / "references" / "templates" / "help-template.md"
    review_path = root / "wilco-plan" / "references" / "templates" / "review-template.md"
    verify_path = root / "wilco-plan" / "references" / "templates" / "verify-template.md"
    truth_path = root / "wilco-plan" / "references" / "templates" / "truth-template.md"
    handoff_path = root / "wilco-plan" / "references" / "templates" / "probe-handoff-template.md"
    agent_path = root / "wilco-plan" / "agents" / "openai.yaml"

    if not skill_path.exists():
        return [f"Missing wilco-plan skill file: {skill_path}"]
    for path, label in (
        (help_path, "help template"),
        (review_path, "review template"),
        (verify_path, "verify template"),
        (truth_path, "truth template"),
        (handoff_path, "probe handoff template"),
        (agent_path, "agent prompt"),
    ):
        if not path.exists():
            failures.append(f"Missing wilco-plan {label}: {path}")

    skill_text = skill_path.read_text(encoding="utf-8")
    for marker in (
        "## Mode Contract",
        "## Execution Readiness Rules",
        "## Verification Rules",
        "Recommended tracking mode",
        "Suggested first slice",
        "Execution readiness risks",
        "Resolved during probe",
        "`verify` is the close-out readiness gate",
        "`verify close`",
        "`verify sync`",
        "`verify replan`",
        "`verified_complete`",
        "`not_complete`",
        "`ambiguous`",
        "A plan is `wilco-exec` ready only when the next smallest unblocked slice can be chosen without guessing",
        "If the current plan is too coarse, too stale, or too ambiguous",
        "make a plan",
        "verify this plan",
        "verify close",
        "verify sync",
        "verify replan",
        "how do I use wilco-plan",
        "If the user's intent could reasonably map to lightweight direct execution instead of tracked planning",
        "user's primary working language",
        "machine-consumed handoff field names stable",
        "keep internal routing and reconciliation heuristics implicit by default",
    ):
        if marker not in skill_text:
            failures.append(f"wilco-plan/SKILL.md missing marker: {marker}")

    if handoff_path.exists():
        handoff_text = handoff_path.read_text(encoding="utf-8")
        for marker in (
            "Optional: Recommended tracking mode",
            "Optional: Suggested first slice",
            "Optional: Execution readiness risks",
            "Optional: Resolved during probe",
            "`Recommended tracking mode`, `Suggested first slice`, `Execution readiness risks`",
        ):
            if marker not in handoff_text:
                failures.append(f"wilco-plan/references/templates/probe-handoff-template.md missing marker: {marker}")

    if help_path.exists():
        help_text = help_path.read_text(encoding="utf-8")
        for marker in (
            "Axis position: the tracked-execution front door",
            "user's primary working language",
        ):
            if marker not in help_text:
                failures.append(f"wilco-plan/references/templates/help-template.md missing marker: {marker}")
        if "- reset" in help_text:
            failures.append("wilco-plan/references/templates/help-template.md should not expose `reset` as a public mode")
        for marker in (
            "## Mode Hints",
            "`verify`: use when you need to check completion against real code and test evidence before close-out",
            "`verify close`: use when you want verification to gate an immediate close-out",
            "`verify sync`: use when you want verification to gate an immediate state refresh",
            "`verify replan`: use when you want verification to gate an immediate execution-contract rewrite",
            "`sync`: use when code moved and the current plan should catch up",
            "`replan`: use when the same slug still applies",
            "`prd`: use when the work now needs or updates `prd_backed` framing",
        ):
            if marker not in help_text:
                failures.append(f"wilco-plan/references/templates/help-template.md missing mode hint marker: {marker}")

    if review_path.exists():
        review_text = review_path.read_text(encoding="utf-8")
        if "`review` must be read-only" not in review_text:
            failures.append("wilco-plan/references/templates/review-template.md missing marker: `review` must be read-only")

    if verify_path.exists():
        verify_text = verify_path.read_text(encoding="utf-8")
        for marker in (
            "## Plan Verify",
            "`verified_complete` | `not_complete` | `ambiguous`",
            "## Evidence",
            "## Open Gaps",
            "## Recommended Action",
            "`direct_execute`",
            "`wilco-plan -> wilco-exec`",
            "## Recommended Next Mode",
            "`verify close`",
            "`verify sync`",
            "`verify replan`",
            "`verify` must be read-only",
        ):
            if marker not in verify_text:
                failures.append(f"wilco-plan/references/templates/verify-template.md missing marker: {marker}")

    if truth_path.exists():
        truth_text = truth_path.read_text(encoding="utf-8")
        if "Use `truth` only when the user explicitly asks" not in truth_text:
            failures.append("wilco-plan/references/templates/truth-template.md missing marker: Use `truth` only when the user explicitly asks")

    if agent_path.exists():
        agent_text = agent_path.read_text(encoding="utf-8")
        for marker in (
            "only default front door",
            "plan_only",
            "probe",
            ".wilco/plans/active",
        ):
            if marker not in agent_text:
                failures.append(f"wilco-plan/agents/openai.yaml missing marker: {marker}")
    if "- `reset`" in skill_text:
        failures.append("wilco-plan/SKILL.md should not expose `reset` as a separate public mode")

    return failures


def validate_workflow_invariants(root: Path) -> list[str]:
    failures: list[str] = []
    required_markers: dict[Path, tuple[str, ...]] = {
        root / "README.md": (
            "`wilco-plan` is the only default user-facing entrypoint",
            "every tracked slug should have an `.wilco/index/<slug>.json` linkage file",
            "agents may route automatically from `wilco-exec` into `wilco-plan close`",
            "lightweight workflow invariant checks",
            "Default Light, Escalate When Needed.",
            "probing and execution are separate escalation axes",
            "## Persistence Policy",
            "## Most Common Paths",
            "## Escalation Hints",
            "## Route Shifts",
            "## Natural Triggers",
            "## Route Visibility",
            "## Install And Uninstall",
            "## Feedback Flow",
            "`wilco-probe grill plan -> wilco-plan`",
            "verify this plan",
            "verify close",
            "verify sync",
            "verify replan",
            "how do I use wilco-probe",
            "how do I use wilco-plan",
            "how do I use wilco-exec",
            "how do I use wilco-feedback",
            "If a natural-language request could reasonably mean more than one of these routes",
            "Skill route: <skill-name>",
            "Route reason: <natural trigger | explicit skill request>",
            "direct_execute -> wilco-plan",
            "auto-classify the report as `bug`, `ux_friction`, `contract_gap`, or `feature_request`",
            "Recommended install path: use `npx skills@latest`.",
            "### Install With `npx skills@latest`",
            "### Uninstall With `npx skills@latest`",
            "### Development Link",
            "### Uninstall",
            "--agent codex",
            "--agent claude-code",
            "Unix-like systems: use `ln -s`",
            "Vercel Skills docs:",
            "Vercel skills guide:",
        ),
        root / "wilco-plan" / "SKILL.md": (
            "only default front door",
            "Do not create a plan",
            "fresh dated slug",
            "delete the active docs and rebuild",
            "Mode: plan_only",
            "probe handoff",
            "Use [scripts/bootstrap_wilco_slug.py]",
            "`close` = delete-and-exit",
            "`cancel` = delete-and-exit",
            "## Mode Contract",
            "## Input Precedence",
            "## Multi-Active Safety Rules",
            "`review` must be strictly read-only",
            "`truth` is manual only",
            "user's primary working language",
            "most recent substantive message",
            "machine-consumed handoff field names stable",
            "## Execution Readiness Rules",
            "## Verification Rules",
            "When work re-enters tracked planning after direct execution",
            "Recommended tracking mode",
            "Suggested first slice",
            "Execution readiness risks",
            "Resolved during probe",
            "Use [references/templates/help-template.md]",
            "Use [references/templates/review-template.md]",
            "Use [references/templates/verify-template.md]",
        ),
        root / "wilco-exec" / "SKILL.md": (
            "not final close-out deletion",
            "route to `wilco-plan close`",
            "route back through `wilco-plan` for reconcile",
            "Prefer `scripts/sync_wilco_index.py`",
            "Use [references/status-vocabulary.md]",
            "Use [references/automation.md]",
            "## Mode Contract",
            "## Output Contract",
            "## Multi-Active Safety Rules",
            "persist plan, index, or temporary reconcile updates to disk",
            "do not guess. Ask for an explicit slug or route back through `wilco-plan review`",
            "include the active source, active slug, and continuation basis in the execution report",
            "Use [references/help-template.md]",
        ),
        root / "wilco-plan" / "references" / "ops" / "bootstrap-levels.md": (
            "create the active plan and the derived index manifest",
        ),
        root / "wilco-plan" / "references" / "rules" / "routing.md": (
            "`wilco-plan` is the only default front door",
            "Do not treat the work as `no-doc`",
            "`upgrade-to-prd-backed`",
            "Prefer dated slugs in `YYYY-MM-DD-topic` form",
            "`related`",
        ),
        root / "wilco-plan" / "references" / "rules" / "closeout-rules.md": (
            "delete active docs",
        ),
        root / "wilco-plan" / "references" / "templates" / "plan-template.md": (
            "Keep the slug stable once tracked",
            "Mode: `prd_backed`",
        ),
        root / "wilco-plan" / "references" / "templates" / "plan-only-template.md": (
            "Keep the slug stable once tracked",
        ),
        root / "wilco-plan" / "references" / "templates" / "prd-template.md": (
            "Mode: prd_backed",
        ),
        root / "wilco-plan" / "references" / "ops" / "reconcile.md": (
            "`upgrade-to-prd-backed`",
            "replace active slug",
            "## Reconcile Summary",
        ),
        root / "wilco-plan" / "references" / "templates" / "probe-handoff-template.md": (
            "Target",
            "Issue classes",
            "Recommended tracking mode",
            "Suggested first slice",
            "Execution readiness risks",
            "Resolved during probe",
            "Accepted decisions",
            "Suggested edits",
        ),
        root / "wilco-exec" / "references" / "help-template.md": (
            "## Wilco Exec Help",
            "user's primary working language",
            "Keep commands and mode literals unchanged.",
            "Axis position: the heavy end of the execution axis",
            "## Inputs",
            "## Behavior",
            "show `Skill route` and `Route reason` in the first visible update when `wilco-exec` is selected",
            "## Safety Rules",
            "do not guess the execution target when multiple active slugs are plausible",
            "## Examples",
        ),
        root / "wilco-plan" / "references" / "templates" / "help-template.md": (
            "## Wilco Plan Help",
            "user's primary working language",
            "Keep commands and mode literals unchanged.",
            "Axis position: the tracked-execution front door",
            "## Modes",
            "## Input Sources",
            "## Input Precedence",
            "## Route Visibility",
            "show `Skill route` and `Route reason` in the first visible update when `wilco-plan` is selected",
            "## Safety Rules",
            "verify",
            "## Examples",
        ),
        root / "wilco-plan" / "references" / "templates" / "review-template.md": (
            "## Plan Review",
            "user's primary working language",
            "Keep commands, mode literals, status literals, and slug/path literals unchanged.",
            "## Current State",
            "## Recommended Next Step",
            "`review` must be read-only",
        ),
        root / "wilco-plan" / "references" / "templates" / "verify-template.md": (
            "## Plan Verify",
            "Completion verdict",
            "## Evidence",
            "## Open Gaps",
            "## Recommended Next Mode",
            "`verify` must be read-only",
        ),
        root / "wilco-plan" / "references" / "templates" / "truth-template.md": (
            "## Truth Extraction",
            "user's primary working language",
            "Keep commands, path literals, and stable field labels unchanged when another workflow consumes them.",
            "## Stable Facts",
            "Use `truth` only when the user explicitly asks",
        ),
        root / "README-zh.md": (
            "## 落盘原则",
            "## 最常用路径",
            "## 升级提示",
            "## Route Shifts",
            "## 自然触发词",
            "## 路由可见性",
            "## 安装与卸载",
            "## 反馈流程",
            "`wilco-probe grill plan -> wilco-plan`",
            "wilco-probe 如何使用",
            "wilco-plan 如何使用",
            "wilco-exec 如何使用",
            "wilco-feedback 如何使用",
            "优先用一句简短确认来消歧",
            "Skill route: <skill-name>",
            "Route reason: <natural trigger | explicit skill request>",
            "默认应根据用户表达和上下文自动归类为 `bug`、`ux_friction`、`contract_gap` 或 `feature_request`",
            "推荐安装方式：使用 `npx skills@latest`。",
            "### 用 `npx skills@latest` 安装",
            "### 开发期 Link",
            "### 卸载",
            "--agent codex",
            "--agent claude-code",
            "Unix-like 系统：使用 `ln -s`",
            "Vercel Skills 文档：",
            "Vercel skills 使用指南：",
            "默认从轻，按需升级。",
        ),
        root / "wilco-probe" / "references" / "help-template.md": (
            "## Wilco Probe Help",
            "## Modes",
            "## Input Model",
            "## Internal State",
            "## Behavior",
            "surface `Skill route` and `Route reason` in the first visible update when `wilco-probe` is selected",
            "## Topic Map Controls",
            "## Plan Targets",
            "## Examples",
            "user's primary working language",
            "Keep commands and mode literals unchanged.",
            "Axis position: the probing axis",
            "bootstrap a light scan when explicit `grill`, `review`, or `resolve` is invoked without usable current probe state",
            "allow a brief solve-and-return inside `grill` for bounded low-risk issues",
            "accept short action modifiers in `grill`",
            "`grill plan`: grill the current active plan as the target object",
            "- grill",
            "- review",
            "- resolve",
            "- retire",
        ),
        root / "wilco-exec" / "references" / "execute-loop.md": (
            "do not perform close-out deletion inside `wilco-exec`",
            "route directly to `wilco-plan close`",
        ),
        root / "wilco-exec" / "references" / "execution-report-template.md": (
            "user's primary working language",
            "Keep commands, status literals, blocker types, and path literals unchanged.",
            "## Execution Step",
            "## Execution State",
            "## Plan Update",
            "## Next Step",
        ),
        root / "wilco-exec" / "references" / "blocker-taxonomy.md": (
            "## Blocked Output Shape",
            "## Blocked",
            "- Type:",
            "- Evidence:",
            "- Unblock:",
            "- Next step:",
        ),
        root / "wilco-exec" / "references" / "status-vocabulary.md": (
            "## Work Status",
            "## Execution Progress",
            "## Alignment Status",
            "## Confidence",
        ),
        root / "wilco-exec" / "references" / "automation.md": (
            "## Sync Derived Index",
            "Use `scripts/sync_wilco_index.py`",
        ),
        root / "wilco-exec" / "scripts" / "sync_wilco_index.py": (
            "Derive minimal .wilco/index manifests from current Wilco artifacts.",
            "from wilco_common import",
        ),
        root / "wilco-exec" / "scripts" / "wilco_common.py": (
            "RELATIONSHIP_KEYS",
            "build_index_manifest",
        ),
        root / "wilco-plan" / "scripts" / "wilco_common.py": (
            "RELATIONSHIP_KEYS",
            "normalize_relationships",
        ),
        root / "wilco-plan" / "scripts" / "validate_wilco_workspace.py": (
            "RELATIONSHIP_KEYS",
            "unexpected relationship key",
        ),
    }

    for path, markers in required_markers.items():
        if not path.exists():
            failures.append(f"Missing workflow invariant file: {path}")
            continue
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                failures.append(f"{path.relative_to(root)} missing marker: {marker}")

    return failures


def validate_contract_map(root: Path) -> list[str]:
    failures: list[str] = []
    file_markers: dict[Path, tuple[str, ...]] = {
        root / "CONTRACTS.md": (
            "## Distribution Assumptions",
            "## Persistence Policy",
            "## User-Facing Vs Internal",
            "## Route Shift Policy",
            "Escalation and de-escalation are both valid workflow moves.",
            "## Verification Authority",
            "## Public Modes Vs Status Values",
            "## External Side Effects",
            "## Contract Layers",
            "## Owners And Derived Forms",
            "## Sync Policy",
            "## Validation Responsibilities",
            "shared scripts",
            "status and decision rules",
            "strong structural templates",
            "Feedback / issue templates",
        ),
        root / "CONTRACTS-zh.md": (
            "## 分发前提",
            "## 落盘原则",
            "## 面向用户 vs 内部状态",
            "## Route Shift 策略",
            "升级和降级都应是合法的 workflow move。",
            "## 核验权威性",
            "## 公开模式名 vs 状态值",
            "## 外部副作用",
            "## 契约层级",
            "## Owner 与派生层",
            "## 同步策略",
            "## Validator 责任",
            "共享脚本",
            "状态与决策规则",
            "强结构模板",
            "feedback / issue 模板",
        ),
    }
    for path, required_markers in file_markers.items():
        if not path.exists():
            failures.append(f"Missing contract map file: {path}")
            continue
        text = path.read_text(encoding="utf-8")
        for marker in required_markers:
            if marker not in text:
                failures.append(f"{path.relative_to(root)} missing marker: {marker}")
    return failures


def skill_root_for_path(path: Path, skill_dirs: list[Path]) -> Path | None:
    for skill_dir in skill_dirs:
        try:
            path.relative_to(skill_dir.resolve())
            return skill_dir.resolve()
        except ValueError:
            continue
    return None


def extract_runtime_reference_tokens(text: str) -> set[str]:
    tokens: set[str] = set()
    for match in MARKDOWN_LINK_RE.finditer(text):
        token = match.group(1)
        if token.startswith(("references/", "scripts/", "agents/", "./", "../")):
            tokens.add(token)
    for match in BACKTICK_PATH_RE.finditer(text):
        tokens.add(match.group(1))
    return tokens


def resolve_runtime_reference(skill_root: Path, current_file: Path, token: str) -> Path:
    if token.startswith(("references/", "scripts/", "agents/")):
        return (skill_root / token).resolve()
    return (current_file.parent / token).resolve()


def validate_runtime_closure(root: Path) -> list[str]:
    failures: list[str] = []
    skill_dirs = [path.resolve() for path in find_skill_dirs(root)]

    for skill_dir in skill_dirs:
        queue: list[Path] = [skill_dir / "SKILL.md"]
        agents_dir = skill_dir / "agents"
        if agents_dir.exists():
            queue.extend(path for path in sorted(agents_dir.rglob("*")) if path.is_file())

        visited: set[Path] = set()
        while queue:
            current = queue.pop(0).resolve()
            if current in visited or not current.exists() or not current.is_file():
                continue
            visited.add(current)

            text = current.read_text(encoding="utf-8")
            for token in sorted(extract_runtime_reference_tokens(text)):
                resolved = resolve_runtime_reference(skill_dir, current, token)
                target_skill = skill_root_for_path(resolved, skill_dirs)
                if target_skill is not None and target_skill != skill_dir:
                    failures.append(
                        f"{current.relative_to(root)} has cross-skill runtime reference `{token}` -> {resolved.relative_to(root)}"
                    )
                    continue
                if target_skill == skill_dir and resolved.is_file() and resolved not in visited:
                    queue.append(resolved)

    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Wilco skills, helper scripts, and obvious content hygiene.")
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]), help="wilco-skills root directory")
    parser.add_argument(
        "--validator",
        default=r"C:\Users\vision\.codex\skills\.system\skill-creator\scripts\quick_validate.py",
        help="Path to quick_validate.py",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    validator = Path(args.validator).resolve()
    skill_dirs = find_skill_dirs(root)
    if not skill_dirs:
        print(f"No skills found under {root}")
        return 1

    python_files = python_files_under(root)
    failures: list[str] = []

    for skill_dir in skill_dirs:
        result = run([sys.executable, str(validator), str(skill_dir)], root)
        if result.returncode != 0:
            failures.append(f"quick_validate failed for {skill_dir.name}: {result.stdout}{result.stderr}".strip())
        else:
            print(f"[ok] quick_validate {skill_dir.name}")

    if python_files:
        compile_result = run([sys.executable, "-m", "py_compile", *[str(path) for path in python_files]], root)
        if compile_result.returncode != 0:
            failures.append(f"py_compile failed:\n{compile_result.stdout}{compile_result.stderr}".strip())
        else:
            print(f"[ok] py_compile {len(python_files)} python files")
            remove_pycache_dirs(root)

    test_file = root / "scripts" / "test_wilco_automation.py"
    if test_file.exists():
        test_result = run([sys.executable, "-m", "unittest", str(test_file)], root)
        if test_result.returncode != 0:
            failures.append(f"automation tests failed:\n{test_result.stdout}{test_result.stderr}".strip())
            remove_pycache_dirs(root)
        else:
            print("[ok] automation tests")
            remove_pycache_dirs(root)

    placeholders = placeholder_hits(root)
    if placeholders:
        failures.append("Placeholder markers remain:\n" + "\n".join(placeholders))
    else:
        print("[ok] no placeholder markers")

    probe_failures = validate_wilco_probe_contract(root)
    if probe_failures:
        failures.append("wilco-probe contract validation failed:\n" + "\n".join(probe_failures))
    else:
        print("[ok] wilco-probe contract")

    feedback_failures = validate_wilco_feedback_contract(root)
    if feedback_failures:
        failures.append("wilco-feedback contract validation failed:\n" + "\n".join(feedback_failures))
    else:
        print("[ok] wilco-feedback contract")

    plan_failures = validate_wilco_plan_contract(root)
    if plan_failures:
        failures.append("wilco-plan contract validation failed:\n" + "\n".join(plan_failures))
    else:
        print("[ok] wilco-plan contract")

    exec_failures = validate_wilco_exec_contract(root)
    if exec_failures:
        failures.append("wilco-exec contract validation failed:\n" + "\n".join(exec_failures))
    else:
        print("[ok] wilco-exec contract")

    workflow_failures = validate_workflow_invariants(root)
    if workflow_failures:
        failures.append("workflow invariant validation failed:\n" + "\n".join(workflow_failures))
    else:
        print("[ok] workflow invariants")

    contract_map_failures = validate_contract_map(root)
    if contract_map_failures:
        failures.append("contract map validation failed:\n" + "\n".join(contract_map_failures))
    else:
        print("[ok] contract map")

    runtime_closure_failures = validate_runtime_closure(root)
    if runtime_closure_failures:
        failures.append("runtime closure validation failed:\n" + "\n".join(runtime_closure_failures))
    else:
        print("[ok] runtime closure")

    cache_dirs = pycache_dirs(root)
    if cache_dirs:
        failures.append("__pycache__ directories remain:\n" + "\n".join(str(path) for path in cache_dirs))
    else:
        print("[ok] no __pycache__ entries")

    if failures:
        print("\nValidation failed:\n")
        for failure in failures:
            print(failure)
            print()
        return 1

    print("\nWilco skills validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
