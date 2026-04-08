#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from wilco_common import (
    architecture_paths,
    index_path,
    plan_archive_path,
    plan_path,
    prd_archive_path,
    prd_path,
    read_json,
    repo_root_from_arg,
    resume_path,
    today_iso,
    update_metadata_text,
    write_json,
)


def prepare_archive_text(
    source_path: Path,
    archive_peer: str | None,
    architecture_hint: str | None,
    completed: str,
    manifest_path: str | None,
) -> str:
    text = source_path.read_text(encoding="utf-8")
    updates: dict[str, tuple[str, str | None]] = {
        "status": ("Status", "archived"),
        "updated": ("Updated", completed),
        "completed": ("Completed", completed),
        "manifest": ("Manifest", manifest_path),
        "current_architecture": ("Current architecture", architecture_hint),
    }

    if source_path.parts[-3:-1] == ("plans", "active"):
        updates["source_prd"] = ("Source PRD", archive_peer)
    elif source_path.parts[-3:-1] == ("prd", "active"):
        updates["related_plan"] = ("Related plan", archive_peer)

    return update_metadata_text(text, updates)


def main() -> int:
    parser = argparse.ArgumentParser(description="Archive an active Wilco slug, clear temporary resume state, and clean index linkage.")
    parser.add_argument("slug", help="Slug to close and archive.")
    parser.add_argument("--repo-root", help="Repository root. Defaults to the current working directory.")
    parser.add_argument("--completed-date", default=today_iso(), help="Completion date in YYYY-MM-DD format.")
    parser.add_argument("--dry-run", action="store_true", help="Print planned changes without writing files.")
    parser.add_argument("--keep-resume", action="store_true", help="Keep the current resume file instead of deleting it.")
    parser.add_argument(
        "--keep-index",
        action="store_true",
        help="Keep an archived index manifest instead of deleting the active coordination file.",
    )
    args = parser.parse_args()

    root = repo_root_from_arg(args.repo_root)
    slug = args.slug
    completed = args.completed_date

    active_plan = plan_path(root, slug)
    active_prd = prd_path(root, slug)
    current_resume = resume_path(root, slug)
    current_index = index_path(root, slug)

    if not active_plan.exists() and not active_prd.exists():
        raise SystemExit(f"No active plan or PRD found for slug '{slug}'.")

    archive_plan = plan_archive_path(root, slug)
    archive_prd = prd_archive_path(root, slug)
    for path in (archive_plan, archive_prd):
        if path.exists():
            raise SystemExit(f"Archive destination already exists: {path}")

    existing_index = read_json(current_index)
    arch_paths = architecture_paths(root, slug, existing_index)
    architecture_hint = ", ".join(arch_paths) if arch_paths else None

    actions: list[str] = []
    if active_plan.exists():
        actions.append(f"archive plan {active_plan} -> {archive_plan}")
    if active_prd.exists():
        actions.append(f"archive prd {active_prd} -> {archive_prd}")
    if current_resume.exists() and not args.keep_resume:
        actions.append(f"delete resume {current_resume}")
    if current_index.exists() and not args.keep_index:
        actions.append(f"delete index {current_index}")
    if current_index.exists() and args.keep_index:
        actions.append(f"rewrite index as archived {current_index}")

    if args.dry_run:
        for action in actions:
            print(f"[dry-run] {action}")
        return 0

    if active_plan.exists():
        archive_plan.parent.mkdir(parents=True, exist_ok=True)
        archive_plan.write_text(
            prepare_archive_text(
                active_plan,
                str(archive_prd.relative_to(root)).replace("\\", "/") if active_prd.exists() else None,
                architecture_hint,
                completed,
                str(current_index.relative_to(root)).replace("\\", "/") if args.keep_index else None,
            ),
            encoding="utf-8",
        )
        active_plan.unlink()
        print(f"Archived plan to {archive_plan}")

    if active_prd.exists():
        archive_prd.parent.mkdir(parents=True, exist_ok=True)
        archive_prd.write_text(
            prepare_archive_text(
                active_prd,
                str(archive_plan.relative_to(root)).replace("\\", "/") if active_plan.exists() or archive_plan.exists() else None,
                architecture_hint,
                completed,
                str(current_index.relative_to(root)).replace("\\", "/") if args.keep_index else None,
            ),
            encoding="utf-8",
        )
        active_prd.unlink()
        print(f"Archived PRD to {archive_prd}")

    if current_resume.exists() and not args.keep_resume:
        current_resume.unlink()
        print(f"Deleted resume {current_resume}")

    if current_index.exists():
        if args.keep_index:
            archived_manifest = {
                "kind": "wilco-linkage-v1",
                "slug": slug,
                "state": {
                    "status": "archived",
                    "progress": "done",
                    "updated": completed,
                },
                "artifacts": {
                    "plan_archive": str(archive_plan.relative_to(root)).replace("\\", "/") if archive_plan.exists() else None,
                    "prd_archive": str(archive_prd.relative_to(root)).replace("\\", "/") if archive_prd.exists() else None,
                    "architecture": arch_paths,
                },
            }
            archived_manifest["artifacts"] = {
                key: value
                for key, value in archived_manifest["artifacts"].items()
                if value not in (None, [], "")
            }
            write_json(current_index, archived_manifest)
            print(f"Archived index {current_index}")
        else:
            current_index.unlink()
            print(f"Deleted index {current_index}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
