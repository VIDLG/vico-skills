#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from wilco_common import (
    architecture_paths,
    index_path,
    plan_path,
    prd_path,
    read_json,
    repo_root_from_arg,
    resume_path,
    today_iso,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Delete active Wilco docs for a closed slug and clear temporary state.")
    parser.add_argument("slug", help="Slug to close and delete from active Wilco docs.")
    parser.add_argument("--repo-root", help="Repository root. Defaults to the current working directory.")
    parser.add_argument("--reason", choices=["done", "cancel"], default="done", help="Why the active docs are being removed.")
    parser.add_argument("--dry-run", action="store_true", help="Print planned changes without writing files.")
    parser.add_argument("--keep-resume", action="store_true", help="Keep the current temporary reconcile file instead of deleting it.")
    args = parser.parse_args()

    root = repo_root_from_arg(args.repo_root)
    slug = args.slug

    active_plan = plan_path(root, slug)
    active_prd = prd_path(root, slug)
    current_resume = resume_path(root, slug)
    current_index = index_path(root, slug)

    if not active_plan.exists() and not active_prd.exists():
        raise SystemExit(f"No active plan or PRD found for slug '{slug}'.")

    existing_index = read_json(current_index)
    arch_paths = architecture_paths(root, slug, existing_index)

    actions: list[str] = []
    if active_plan.exists():
        actions.append(f"delete active plan {active_plan}")
    if active_prd.exists():
        actions.append(f"delete active prd {active_prd}")
    if current_resume.exists() and not args.keep_resume:
        actions.append(f"delete resume {current_resume}")
    if current_index.exists():
        actions.append(f"delete index {current_index}")
    if not arch_paths:
        actions.append("confirm architecture extraction is not needed")

    if args.dry_run:
        print(f"[dry-run] reason={args.reason}")
        for action in actions:
            print(f"[dry-run] {action}")
        return 0

    if active_plan.exists():
        active_plan.unlink()
        print(f"Deleted active plan {active_plan} ({args.reason})")

    if active_prd.exists():
        active_prd.unlink()
        print(f"Deleted active PRD {active_prd} ({args.reason})")

    if current_resume.exists() and not args.keep_resume:
        current_resume.unlink()
        print(f"Deleted resume {current_resume}")

    if current_index.exists():
        current_index.unlink()
        print(f"Deleted index {current_index}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
