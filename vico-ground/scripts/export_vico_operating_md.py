#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


def find_active_slug(repo_root: Path) -> tuple[str | None, str | None, str | None]:
    plan_root = repo_root / ".vico" / "plans" / "active"
    if not plan_root.exists():
        return None, None, None
    plans = sorted(plan_root.glob("*.md"))
    if len(plans) != 1:
        return None, None, None
    plan = plans[0]
    slug = plan.stem
    prd = repo_root / ".vico" / "prd" / "active" / f"{slug}.md"
    return slug, f".vico/plans/active/{plan.name}", f".vico/prd/active/{prd.name}" if prd.exists() else None


def build_markdown(target_name: str, active_slug: str | None, plan_path: str | None, prd_path: str | None) -> str:
    lines = [
        f"# {target_name}",
        "",
        "## Vico Operating Brief",
        "",
        "Use this repo with explicit clarification, minimal planning, surgical edits, and verification-driven execution.",
        "",
        "## Clarification Discipline",
        "",
        "- Do not assume missing intent when a short clarification question would remove real ambiguity.",
        "- Do not hide confusion behind overconfident prose.",
        "- Surface tradeoffs explicitly when multiple live options still exist.",
        "- If uncertain, ask rather than guess.",
        "",
        "## Simplicity Discipline",
        "",
        "- Build the minimum contract or code needed to solve the current problem.",
        "- Do not add speculative abstractions, phases, or artifacts just because they might help later.",
        "- Prefer the smallest plan shape that still supports reliable execution.",
        "",
        "## Surgical Edit Discipline",
        "",
        "- Touch only what you must to complete the current step safely.",
        "- Clean up only your own mess unless scope is explicitly expanded.",
        "- Every changed line should trace directly to the current objective.",
        "",
        "## Success Criteria Discipline",
        "",
        "- Define success criteria before treating work as done.",
        "- Loop until verified; implementation alone is not completion.",
        "- If verification still shows open gaps, continue or re-enter planning instead of claiming done.",
        "",
        "## Repo-Local Workflow",
        "",
        "- Use `vico-ground` to clarify, scan, align, reframe, map, surface tradeoffs, and pressure-test before action.",
        "- Use `vico-ground challenge` when adversarial review or counterexamples are needed.",
        "- Use `vico-plan` to create, sync, verify, or reshape tracked work under `.vico/`.",
        "- Use `vico-exec` for persistent execution against an active plan.",
        "- Use `vico-exec cc` when Claude Code should drive a stronger outer execution loop.",
        "- Do not delete active `.vico` docs without explicit user confirmation.",
        "",
        "## Vico Active Context",
        "",
    ]
    if active_slug and plan_path:
        lines.extend(
            [
                f"- Active slug: `{active_slug}`",
                f"- Active plan: `{plan_path}`",
            ]
        )
        if prd_path:
            lines.append(f"- Source PRD: `{prd_path}`")
    else:
        lines.append("- No single active slug was resolved during export.")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Export a repo-local Vico operating brief to AGENTS.md or CLAUDE.md.")
    parser.add_argument("target", nargs="?", default="AGENTS.md", help="Target markdown file to create, usually AGENTS.md or CLAUDE.md")
    parser.add_argument("--repo-root", default=".", help="Repository root that contains .vico/")
    parser.add_argument("--stdout", action="store_true", help="Print the generated markdown instead of writing a file")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite the target file if it already exists")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    target_path = (repo_root / args.target).resolve()
    active_slug, plan_path, prd_path = find_active_slug(repo_root)
    markdown = build_markdown(target_path.name, active_slug, plan_path, prd_path)

    if args.stdout:
        print(markdown)
        return 0

    target_path.parent.mkdir(parents=True, exist_ok=True)
    if target_path.exists() and not args.overwrite:
        raise SystemExit(f"Refusing to overwrite existing file: {target_path}")
    target_path.write_text(markdown + "\n", encoding="utf-8")
    print(f"Wrote {target_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
