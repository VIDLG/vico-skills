#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from vico_common import active_slugs, detect_metadata, plan_path, prd_path, repo_root_from_arg, write_text


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export a repo-local Vico operating brief to AGENTS.md or CLAUDE.md."
    )
    parser.add_argument(
        "target",
        nargs="?",
        default="AGENTS.md",
        help="Target markdown file to create, usually AGENTS.md or CLAUDE.md",
    )
    parser.add_argument("--repo-root", help="Repository root that contains .vico/")
    parser.add_argument("--slug", help="Optional active slug to anchor the export")
    parser.add_argument("--stdout", action="store_true", help="Print the generated markdown instead of writing a file")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite the target file if it already exists")
    return parser.parse_args()


def resolve_active_slug(root: Path, requested_slug: str | None) -> str | None:
    if requested_slug:
        return requested_slug
    slugs = sorted(active_slugs(root))
    if len(slugs) == 1:
        return slugs[0]
    return None


def load_active_context(root: Path, slug: str | None) -> dict[str, str]:
    context: dict[str, str] = {}
    if not slug:
        return context

    plan = plan_path(root, slug)
    if plan.exists():
        metadata = detect_metadata(plan)
        context["active_slug"] = slug
        context["plan_mode"] = metadata.get("mode", "plan_only")
        context["plan_status"] = metadata.get("status", "in_progress")
        context["plan_path"] = ".vico/plans/active/" + plan.name

    prd = prd_path(root, slug)
    if prd.exists():
        context["prd_path"] = ".vico/prd/active/" + prd.name
    return context


def build_markdown(target_name: str, context: dict[str, str]) -> str:
    title = target_name
    active_slug = context.get("active_slug")
    plan_mode = context.get("plan_mode")
    plan_status = context.get("plan_status")
    plan_path_value = context.get("plan_path")
    prd_path_value = context.get("prd_path")

    active_block = [
        "## Vico Active Context",
        "",
    ]
    if active_slug and plan_path_value:
        active_block.extend(
            [
                f"- Active slug: `{active_slug}`",
                f"- Active plan: `{plan_path_value}`",
                f"- Active mode: `{plan_mode}`",
                f"- Active status: `{plan_status}`",
            ]
        )
        if prd_path_value:
            active_block.append(f"- Source PRD: `{prd_path_value}`")
    else:
        active_block.append("- No single active slug was resolved during export.")

    lines = [
        f"# {title}",
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
        "- Use `vico-grill` for freeform pressure-testing before repository evidence matters.",
        "- Use `vico-probe` when repo plans, code, PRDs, or files must be inspected against repository reality.",
        "- Use `vico-plan` to create, sync, verify, or reshape tracked work under `.vico/`.",
        "- Use `vico-exec` for persistent execution against an active plan.",
        "- Use `vico-exec cc` when Claude Code should drive a stronger outer execution loop.",
        "- Do not delete active `.vico` docs without explicit user confirmation.",
        "",
        *active_block,
        "",
    ]
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    args = parse_args()
    root = repo_root_from_arg(args.repo_root)
    target_path = (root / args.target).resolve()
    slug = resolve_active_slug(root, args.slug)
    context = load_active_context(root, slug)
    text = build_markdown(target_path.name, context)

    if args.stdout:
        print(text, end="")
        return 0

    write_text(target_path, text, overwrite=args.overwrite)
    print(f"Wrote {target_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
