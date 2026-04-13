#!/usr/bin/env python3
from __future__ import annotations

import ast
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
    return sorted(
        path
        for path in root.iterdir()
        if path.is_dir() and (path / "SKILL.md").exists()
    )


def python_files_under(path: Path) -> list[Path]:
    if not path.exists():
        return []
    return sorted(
        file for file in path.rglob("*.py") if "__pycache__" not in file.parts
    )


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


SKILL_CONTRACTS = {
    "vico-ground": {
        "display_name": "Vico Ground",
        "sections": [
            "## Agent Summary",
            "## Public Moves",
            "## Controller Rules",
            "## Stop Rule",
            "## Minimal State Model",
            "## Output Contract",
        ],
        "tokens": ["`scan`", "`clarify`", "`stress`", "`handoff`"],
    },
    "vico-plan": {
        "display_name": "Vico Plan",
        "sections": [
            "## Agent Summary",
            "## Simplicity Discipline",
            "## Forward-Only Planning Discipline",
            "## Mode Contract",
            "## Workflow",
            "## Output Contract",
        ],
        "tokens": ["`vico-ground` handoff", "`plan_only`", "`prd_backed`"],
    },
    "vico-exec": {
        "display_name": "Vico Exec",
        "sections": [
            "## Agent Summary",
            "## Surgical Execution Discipline",
            "## Success Criteria Discipline",
            "## Mode Contract",
            "## Execution Loop",
            "## Claude Code",
        ],
        "tokens": ["`cc`", "Loop until verified", "`vico-ground` handoffs"],
    },
    "vico-feedback": {
        "display_name": "Vico Feedback",
        "sections": [
            "## Agent Summary",
            "## Goals",
            "## Inputs",
            "## Workflow",
            "## Safety Rules",
            "## Output Contract",
        ],
        "tokens": ["GitHub issue draft", "explicit user confirmation"],
    },
    "vico-ops": {
        "display_name": "Vico Ops",
        "sections": [
            "## Agent Summary",
            "## Modes",
            "## Control Rules",
            "## Multi-Active Safety Rules",
            "## Repo-Local Operations",
            "## Output Contract",
        ],
        "tokens": ["`bootstrap`", "`sync`", "`close`", "`validate`", "`runtime/cli/`"],
    },
}

CORE_DOCS = {
    "README.md": ("# vico-skills", "## Start Here", "## Validation"),
    "README-zh.md": ("# vico-skills", "## 从这里开始", "## 校验"),
    "CONTRACTS.md": ("# Vico Contracts", "## Contract Layers", "## Sync Policy"),
    "CONTRACTS-zh.md": ("# Vico 契约映射", "## 契约层级", "## 同步策略"),
    "TRIGGERS.md": ("# Trigger Examples", "## Routing Order", "## Anti-Patterns"),
    "TRIGGERS-zh.md": ("# 触发示例矩阵", "## 路由顺序", "## 反模式"),
    "CONSENSUS.md": ("# Consensus Models", "## Practical Consensus Moves", "## Anti-Patterns"),
    "CONSENSUS-zh.md": ("# 共识模型", "## 可用的共识动作", "## 反模式"),
}

REQUIRED_PATHS = [
    "scripts/export_vico_operating_md.py",
    "scripts/sync_shared_vico_runtime.py",
    "scripts/sync_openai_agents.py",
    "runtime/cli/bootstrap_vico_slug.py",
    "runtime/cli/close_vico_slug.py",
    "runtime/cli/sync_vico_headers.py",
    "runtime/cli/sync_vico_index.py",
    "runtime/cli/validate_vico_workspace.py",
    "runtime/vico_artifacts/vico_common.py",
    "adapters/claude/claude_exec_runner.py",
    "adapters/claude/session_start_hook.ps1",
    "adapters/claude/stop_hook.ps1",
    "vico-ground/references/output-format.md",
    "vico-plan/references/templates/architecture-template.md",
    "vico-ops/references/help-template.md",
    "vico-plan/references/templates/ground-handoff-template.md",
    "vico-exec/references/runner.md",
    "vico-exec/references/cc-operator.md",
]

AGENT_SUMMARY_MARKERS = [
    "- `Display name`:",
    "- `Short description`:",
    "- `Default prompt`:",
]


def validate_skill_contracts(root: Path) -> list[str]:
    failures: list[str] = []
    for skill_name, contract in SKILL_CONTRACTS.items():
        path = root / skill_name / "SKILL.md"
        if not path.exists():
            failures.append(f"Missing skill contract: {path}")
            continue
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        frontmatter = "\n".join(lines[:8])
        for marker in ("---", f"name: {skill_name}", "description:"):
            if marker not in frontmatter:
                failures.append(f"{path.relative_to(root)} missing frontmatter marker: {marker}")
        for section in contract["sections"]:
            if section not in text:
                failures.append(f"{path.relative_to(root)} missing section: {section}")
        for marker in AGENT_SUMMARY_MARKERS:
            if marker not in text:
                failures.append(f"{path.relative_to(root)} missing agent summary field: {marker}")
        display_marker = f"- `Display name`: `{contract['display_name']}`"
        if display_marker not in text:
            failures.append(f"{path.relative_to(root)} missing display name marker: {display_marker}")
        for token in contract["tokens"]:
            if token not in text:
                failures.append(f"{path.relative_to(root)} missing contract token: {token}")
    return failures


def validate_core_docs(root: Path) -> list[str]:
    failures: list[str] = []
    for relative_path, markers in CORE_DOCS.items():
        path = root / relative_path
        if not path.exists():
            failures.append(f"Missing core doc: {path}")
            continue
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                failures.append(f"{relative_path} missing core doc marker: {marker}")
    return failures


def validate_required_paths(root: Path) -> list[str]:
    failures: list[str] = []
    for relative_path in REQUIRED_PATHS:
        path = root / relative_path
        if not path.exists():
            failures.append(f"Missing required path: {path}")
    return failures


def validate_generated_forms(root: Path) -> list[str]:
    failures: list[str] = []
    checks = [
        [sys.executable, str(root / "scripts" / "sync_shared_vico_runtime.py"), "--root", str(root), "--check"],
        [sys.executable, str(root / "scripts" / "sync_openai_agents.py"), "--root", str(root), "--check"],
    ]
    for cmd in checks:
        result = run(cmd, root)
        if result.returncode != 0:
            failures.append(
                "generated form drift:\n"
                + " ".join(cmd)
                + "\n"
                + (result.stdout + result.stderr).strip()
            )
    return failures


def validate_thin_wrappers(root: Path) -> list[str]:
    failures: list[str] = []
    wrappers = {
        "vico-plan/scripts/bootstrap_vico_slug.py": "runtime/cli/bootstrap_vico_slug.py",
        "vico-plan/scripts/close_vico_slug.py": "runtime/cli/close_vico_slug.py",
        "vico-plan/scripts/sync_vico_headers.py": "runtime/cli/sync_vico_headers.py",
        "vico-plan/scripts/sync_vico_index.py": "runtime/cli/sync_vico_index.py",
        "vico-plan/scripts/validate_vico_workspace.py": "runtime/cli/validate_vico_workspace.py",
        "vico-exec/scripts/claude_exec_runner.py": "adapters/claude/claude_exec_runner.py",
    }
    for relative_path, owner in wrappers.items():
        path = root / relative_path
        if not path.exists():
            failures.append(f"Missing wrapper: {path}")
            continue
        text = path.read_text(encoding="utf-8")
        for marker in ("runpy.run_path", owner):
            if marker not in text:
                failures.append(f"{relative_path} missing wrapper marker: {marker}")
    return failures


def validate_current_contracts(root: Path) -> list[str]:
    failures: list[str] = []
    failures.extend(validate_skill_contracts(root))
    failures.extend(validate_core_docs(root))
    failures.extend(validate_required_paths(root))
    failures.extend(validate_generated_forms(root))
    failures.extend(validate_thin_wrappers(root))
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
            queue.extend(
                path for path in sorted(agents_dir.rglob("*")) if path.is_file()
            )
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
                if (
                    target_skill == skill_dir
                    and resolved.is_file()
                    and resolved not in visited
                ):
                    queue.append(resolved)
    return failures


def validate_shared_script_parity(root: Path) -> list[str]:
    failures: list[str] = []
    owner = root / "runtime" / "vico_artifacts" / "vico_common.py"
    closures = [
        root / "vico-plan" / "scripts" / "vico_common.py",
        root / "vico-exec" / "scripts" / "vico_common.py",
    ]
    if not owner.exists():
        return [f"Missing shared script owner: {owner}"]
    missing_closures = [path for path in closures if not path.exists()]
    if missing_closures:
        return [f"Missing shared script closure: {path}" for path in missing_closures]

    owner_text = ast.dump(
        ast.parse(owner.read_text(encoding="utf-8")), include_attributes=False
    )
    for closure in closures:
        closure_text = ast.dump(
            ast.parse(closure.read_text(encoding="utf-8")), include_attributes=False
        )
        if owner_text != closure_text:
            failures.append(
                "shared script drift: "
                f"{closure.relative_to(root)} must stay in semantic parity with owner source "
                f"{owner.relative_to(root)}"
            )
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate Vico skills, helper scripts, and basic content hygiene."
    )
    parser.add_argument(
        "--root",
        default=str(Path(__file__).resolve().parents[1]),
        help="vico-skills root directory",
    )
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
            failures.append(
                f"quick_validate failed for {skill_dir.name}: {result.stdout}{result.stderr}".strip()
            )
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
            failures.append(
                f"py_compile failed:\n{compile_result.stdout}{compile_result.stderr}".strip()
            )
        else:
            print(f"[ok] py_compile {len(python_files)} python files")
        shutil.rmtree(pycache_prefix, ignore_errors=True)
        remove_pycache_dirs(root)

    test_file = root / "scripts" / "test_vico_automation.py"
    if test_file.exists():
        test_result = run([sys.executable, str(test_file)], root)
        if test_result.returncode != 0:
            failures.append(
                f"automation tests failed:\n{test_result.stdout}{test_result.stderr}".strip()
            )
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
        failures.append(
            "current contract validation failed:\n" + "\n".join(contract_failures)
        )
    else:
        print("[ok] current skill contracts")

    runtime_closure_failures = validate_runtime_closure(root)
    if runtime_closure_failures:
        failures.append(
            "runtime closure validation failed:\n" + "\n".join(runtime_closure_failures)
        )
    else:
        print("[ok] runtime closure")

    shared_script_parity_failures = validate_shared_script_parity(root)
    if shared_script_parity_failures:
        failures.append(
            "shared script parity validation failed:\n"
            + "\n".join(shared_script_parity_failures)
        )
    else:
        print("[ok] shared script parity")

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
