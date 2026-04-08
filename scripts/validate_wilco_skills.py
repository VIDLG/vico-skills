#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

PLACEHOLDER_MARKERS = ("[TODO",)


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


def validate_wilco_grill_contract(root: Path) -> list[str]:
    failures: list[str] = []
    skill_path = root / "wilco-grill" / "SKILL.md"
    reference_path = root / "wilco-grill" / "references" / "output-format.md"
    agent_path = root / "wilco-grill" / "agents" / "openai.yaml"

    if not skill_path.exists():
        return [f"Missing wilco-grill skill file: {skill_path}"]
    if not reference_path.exists():
        failures.append(f"Missing wilco-grill output reference: {reference_path}")
    if not agent_path.exists():
        failures.append(f"Missing wilco-grill agent prompt: {agent_path}")

    skill_text = skill_path.read_text(encoding="utf-8")
    required_skill_markers = (
        "## Question Ordering Rules",
        "## Output Contract",
        "### Core Sections",
        "### Optional Sections",
        "## Stop Conditions",
        "## Summary Contract",
        "### Core Summary Sections",
        "### Optional Summary Sections",
        "## Anti-Patterns",
        "[references/output-format.md](references/output-format.md)",
        "`Question N: <question text>`",
        "`Accepted decisions`",
        "`Suggested edits`",
    )
    for marker in required_skill_markers:
        if marker not in skill_text:
            failures.append(f"wilco-grill/SKILL.md missing marker: {marker}")

    if reference_path.exists():
        reference_text = reference_path.read_text(encoding="utf-8")
        required_reference_markers = (
            "## Minimal Question Template",
            "## Expanded Question Example",
            "## Final Summary Example",
            "Question 7:",
            "Accepted decisions",
        )
        for marker in required_reference_markers:
            if marker not in reference_text:
                failures.append(f"wilco-grill/references/output-format.md missing marker: {marker}")

    if agent_path.exists():
        agent_text = agent_path.read_text(encoding="utf-8")
        required_agent_markers = (
            "SKILL.md",
            "higher-impact branches before formatting details",
        )
        for marker in required_agent_markers:
            if marker not in agent_text:
                failures.append(f"wilco-grill/agents/openai.yaml missing marker: {marker}")
        forbidden_agent_markers = (
            "Recommended answer",
            "Why it matters",
            "Decision dependency",
            "Write-back target",
        )
        for marker in forbidden_agent_markers:
            if marker in agent_text:
                failures.append(f"wilco-grill/agents/openai.yaml should not duplicate detailed contract marker: {marker}")

    return failures


def validate_workflow_invariants(root: Path) -> list[str]:
    failures: list[str] = []
    required_markers: dict[Path, tuple[str, ...]] = {
        root / "README.md": (
            "new tracked work enters through `wilco-init`",
            "every tracked slug should have an `.wilco/index/<slug>.json` linkage file",
            "agents may route automatically from `wilco-execute` into `wilco-cleanup`",
            "lightweight workflow invariant checks",
        ),
        root / "wilco-plan" / "SKILL.md": (
            "use `wilco-init` first",
            "do not treat it as `no-doc`",
        ),
        root / "wilco-prd" / "SKILL.md": (
            "hard escalation gate",
            "hand off to `wilco-init`",
        ),
        root / "wilco-execute" / "SKILL.md": (
            "not final archive handling",
            "route to `wilco-cleanup`",
        ),
        root / "wilco-cleanup" / "SKILL.md": (
            "Users should not need to remember this skill manually",
        ),
        root / "wilco-docs" / "SKILL.md": (
            "new tracked work enters through `wilco-init`",
            "index` exists for tracked slugs",
        ),
        root / "wilco-init" / "references" / "bootstrap-levels.md": (
            "create the active plan and the derived index manifest",
        ),
        root / "wilco-docs" / "references" / "decision-tree.md": (
            "tracked work should enter through `wilco-init`",
            "Do not treat the work as `no-doc`",
        ),
        root / "wilco-execute" / "references" / "execute-loop.md": (
            "do not perform archive handling inside `wilco-execute`",
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

    grill_failures = validate_wilco_grill_contract(root)
    if grill_failures:
        failures.append("wilco-grill contract validation failed:\n" + "\n".join(grill_failures))
    else:
        print("[ok] wilco-grill contract")

    workflow_failures = validate_workflow_invariants(root)
    if workflow_failures:
        failures.append("workflow invariant validation failed:\n" + "\n".join(workflow_failures))
    else:
        print("[ok] workflow invariants")

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
