#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
import shutil
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
        if file.suffix.lower() not in {".md", ".yaml", ".yml", ".json", ".txt", ".py"}:
            continue
        text = file.read_text(encoding="utf-8")
        for line_number, line in enumerate(text.splitlines(), start=1):
            if file.name == "validate_vico_skills.py" and "PLACEHOLDER_MARKERS" in line:
                continue
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


def validate_skill_markers(root: Path, relative_path: str, markers: tuple[str, ...]) -> list[str]:
    failures: list[str] = []
    path = root / relative_path
    if not path.exists():
        return [f"Missing file: {path}"]
    text = path.read_text(encoding="utf-8")
    for marker in markers:
        if marker not in text:
            failures.append(f"{relative_path} missing marker: {marker}")
    return failures


def validate_current_contracts(root: Path) -> list[str]:
    failures: list[str] = []
    required: dict[str, tuple[str, ...]] = {
        "vico-ground/SKILL.md": (
            "shared-ground construction workflow",
            "Treat short repo-orientation requests as strong `vico-ground` signals by default",
            "## Theory Basis",
            "## Grounding Principles",
            "## State Model",
            "Accepted Facts",
            "Active Assumptions",
            "Interpretations",
            "Findings",
            "Preferences",
            "Issue Bank",
            "Tradeoffs",
            "Commitments",
            "Ground Handoff",
            "## Epistemic Status Model",
            "`fact`",
            "`assumption`",
            "`interpretation`",
            "`preference`",
            "`commitment`",
            "## Epistemic Transition Rules",
            "`assumption -> fact`",
            "`preference -> commitment`",
            "## Moves",
            "`clarify`",
            "`scan`",
            "`map`",
            "`align`",
            "`reframe`",
            "`tradeoff`",
            "`grill`",
            "`challenge`",
            "`export-md`",
            "`review`",
            "`resolve`",
            "## Move Selection Rubric",
            "ambiguity_reduction",
            "verification_impact",
            "Do not treat every `Finding` as an `Issue`",
        ),
        "vico-ground/references/help-template.md": (
            "## Vico Ground Help",
            "- clarify",
            "- reframe",
            "- tradeoff",
            "- grill",
            "- challenge",
            "- export-md",
            "keep findings and issues separate",
        ),
        "vico-ground/agents/openai.yaml": (
            "Think before acting",
            "Prefer the minimum grounding move",
        ),
        "vico-ground/scripts/export_vico_operating_md.py": (
            "Export a repo-local Vico operating brief to AGENTS.md or CLAUDE.md.",
            "## Vico Operating Brief",
            "Use `vico-ground` to clarify, scan, align, reframe, map, surface tradeoffs, and pressure-test before action.",
        ),
        "vico-ground/references/output-format.md": (
            "# Vico Ground Output Format",
            "## Scan Example",
            "## Ground Handoff Example",
            "Findings",
            "Preferences",
            "Commitments",
            "Invalidation triggers",
        ),
        "vico-plan/SKILL.md": (
            "## Simplicity Discipline",
            "Treat tracked-work controller intent as the main routing signal",
            "`vico-ground` handoff",
        ),
        "vico-plan/references/templates/help-template.md": (
            "`verify close`",
            "`sync`: use when code moved and the current plan should catch up",
        ),
        "vico-plan/agents/openai.yaml": (
            "Apply simplicity first",
            "prefer the smallest execution contract",
            "avoid speculative phases or abstractions",
        ),
        "vico-plan/references/templates/ground-handoff-template.md": (
            "# Ground Handoff Template",
            "## Ground Handoff",
            "Optional: Active assumptions",
            "Optional: Preferences",
            "Optional: Tradeoffs",
            "Optional: Commitments",
            "Optional: Invalidation triggers",
            "strong downstream inputs",
            "soft context inputs",
        ),
        "vico-exec/SKILL.md": (
            "`cc`",
            "launch the bundled Claude Code runner loop against the active plan",
            "## Surgical Execution Discipline",
            "## Success Criteria Discipline",
            "Loop until verified",
            "Treat persistent implementation intent as the main routing signal",
            "`vico-ground` handoffs",
        ),
        "vico-exec/references/help-template.md": (
            "## Modes",
            "- cc",
            "vico-exec cc",
            "run this with cc",
            "handoff to cc",
        ),
        "vico-exec/agents/openai.yaml": (
            "Use surgical changes and goal-driven execution",
            "define success criteria before calling work done",
            "loop until verification evidence is strong enough",
        ),
        "vico-exec/references/automation.md": (
            "## Claude Runner Loop",
            "claude_exec_runner.py",
        ),
        "vico-exec/references/runner.md": (
            "## Claude Runner",
            "continue",
            "stale_plan",
            "cc-operator.md",
        ),
        "vico-exec/references/cc-operator.md": (
            "## When To Use `vico-exec cc`",
            "## Exit Codes",
            "## Recommended Operator Flow",
            "## Hook Vs Runner",
            "## Example Outcomes",
            "`0`",
            "`4`",
        ),
        "vico-exec/scripts/claude_exec_runner.py": (
            "RUNNER_SCHEMA",
            "claude",
            "stale_plan",
        ),
        "vico-feedback/SKILL.md": (
            "GitHub issue draft",
            "Treat feedback-about-the-workflow intent as the main routing signal",
            "how do I use vico-feedback",
        ),
        "vico-feedback/agents/openai.yaml": (
            "Think before filing",
            "separate workflow feedback from unrelated repository bugs",
            "prefer the smallest accurate draft",
        ),
        "README.md": (
            "`vico-ground`",
            "Trigger examples: [TRIGGERS.md](TRIGGERS.md)",
            "problem framing and execution structure are separate escalation axes",
            "### Escalation Map",
            "Codex: vico-plan -> Claude Code: vico-exec",
            "vico-ground export-md AGENTS.md",
            "## External Influences",
            "forrestchang/andrej-karpathy-skills",
            "### Karpathy Mapping",
            "Think Before Coding",
            "Surgical Changes",
            "Consensus guide: [CONSENSUS.md](CONSENSUS.md)",
            "## Start Here",
            "Three common paths",
            "Route by intent cluster first, phrase match second.",
        ),
        "README-zh.md": (
            "`vico-ground`",
            "触发示例: [TRIGGERS-zh.md](TRIGGERS-zh.md)",
            "Codex: vico-plan -> Claude Code: vico-exec",
            "共识模型参考: [CONSENSUS-zh.md](CONSENSUS-zh.md)",
            "### Karpathy 映射",
            "Think Before Coding",
            "Surgical Changes",
            "## 从这里开始",
            "三条最常见路径",
            "应先按意图簇路由，再用短语匹配补召回。",
        ),
        "TRIGGERS.md": (
            "# Trigger Examples",
            "## Routing Order",
            "Route by intent cluster first.",
            "## Intent Clusters",
            "Repo orientation, architecture scan, alignment, mapping, challenge, review",
            "Persistent implementation continuation",
            "## Example Decisions",
            "## Short Clarification Patterns",
            "## Anti-Patterns",
        ),
        "TRIGGERS-zh.md": (
            "# 触发示例矩阵",
            "## 路由顺序",
            "先按意图簇路由。",
            "## 意图簇",
            "仓库摸底、架构扫描、对齐、建图、challenge、review",
            "持续推进实现",
            "## 路由示例",
            "## 短确认模板",
            "## 反模式",
        ),
        "CONSENSUS.md": (
            "# Consensus Models",
            "### Common Ground",
            "### Conversational Grounding",
            "### Sensemaking",
            "### Deliberation And Argumentation",
            "### Negotiation And Preference Reconciliation",
            "### Vocabulary And Ontology Alignment",
            "## Practical Consensus Moves",
            "## Theory To Move Mapping",
            "## Failure Patterns",
            "## Anti-Patterns",
        ),
        "CONSENSUS-zh.md": (
            "# 共识模型",
            "### Common Ground",
            "### Conversational Grounding",
            "### Sensemaking",
            "## 可用的共识动作",
            "## 理论到 Move 的映射表",
            "## 失败模式",
            "## 反模式",
        ),
    }
    for relative_path, markers in required.items():
        failures.extend(validate_skill_markers(root, relative_path, markers))
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
    parser = argparse.ArgumentParser(description="Validate Vico skills, helper scripts, and basic content hygiene.")
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]), help="vico-skills root directory")
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

    failures: list[str] = []

    for skill_dir in skill_dirs:
        result = run([sys.executable, str(validator), str(skill_dir)], root)
        if result.returncode != 0:
            failures.append(f"quick_validate failed for {skill_dir.name}: {result.stdout}{result.stderr}".strip())
        else:
            print(f"[ok] quick_validate {skill_dir.name}")

    python_files = python_files_under(root)
    if python_files:
        pycache_prefix = root / ".tmp-pycache"
        shutil.rmtree(pycache_prefix, ignore_errors=True)
        pycache_prefix.mkdir(exist_ok=True)
        compile_env = dict(os.environ)
        compile_env["PYTHONPYCACHEPREFIX"] = str(pycache_prefix)
        compile_result = subprocess.run(
            [sys.executable, "-m", "py_compile", *[str(path) for path in python_files]],
            cwd=root,
            text=True,
            capture_output=True,
            env=compile_env,
        )
        if compile_result.returncode != 0:
            failures.append(f"py_compile failed:\n{compile_result.stdout}{compile_result.stderr}".strip())
        else:
            print(f"[ok] py_compile {len(python_files)} python files")
        shutil.rmtree(pycache_prefix, ignore_errors=True)
        remove_pycache_dirs(root)

    test_file = root / "scripts" / "test_vico_automation.py"
    if test_file.exists():
        test_result = run([sys.executable, str(test_file)], root)
        if test_result.returncode != 0:
            failures.append(f"automation tests failed:\n{test_result.stdout}{test_result.stderr}".strip())
        else:
            print("[ok] automation tests")
        remove_pycache_dirs(root)

    placeholders = placeholder_hits(root)
    if placeholders:
        failures.append("Placeholder markers remain:\n" + "\n".join(placeholders))
    else:
        print("[ok] no placeholder markers")

    contract_failures = validate_current_contracts(root)
    if contract_failures:
        failures.append("current contract validation failed:\n" + "\n".join(contract_failures))
    else:
        print("[ok] current skill contracts")

    runtime_closure_failures = validate_runtime_closure(root)
    if runtime_closure_failures:
        failures.append("runtime closure validation failed:\n" + "\n".join(runtime_closure_failures))
    else:
        print("[ok] runtime closure")

    if pycache_dirs(root):
        failures.append("Unexpected __pycache__ entries remain")
    else:
        print("[ok] no __pycache__ entries")

    if failures:
        print("\nValidation failed:\n")
        print("\n\n".join(failures))
        return 1

    print("\nVico skills validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
