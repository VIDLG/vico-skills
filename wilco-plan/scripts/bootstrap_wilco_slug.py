#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PLAN_SCRIPTS = SCRIPT_DIR
import sys

if str(PLAN_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(PLAN_SCRIPTS))

from wilco_common import (  # noqa: E402
    architecture_doc_path,
    build_index_manifest,
    ensure_wilco_layout,
    index_path,
    plan_path,
    prd_path,
    read_json,
    repo_root_from_arg,
    sync_active_headers_for_slug,
    today_iso,
    write_json,
    write_text,
)

DATED_SLUG_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-[a-z0-9][a-z0-9-]*$")


def dated_slug(raw_slug: str, current_date: str) -> str:
    slug = raw_slug.strip()
    if DATED_SLUG_RE.match(slug):
        return slug
    return f"{current_date}-{slug}"


def plan_only_text(title: str, slug: str, current_date: str) -> str:
    return (
        f"# Plan: {title}\n\n"
        f"> Status: `in_progress`\n"
        f"> Mode: `plan_only`\n"
        f"> Progress: `not_started`\n"
        f"> Slug: `{slug}`\n"
        f"> Created: `{current_date}`\n"
        f"> Updated: `{current_date}`\n\n"
        "## Goal\n\n"
        "Describe the concrete task outcome in one short paragraph.\n\n"
        "## Constraints\n\n"
        "- ...\n\n"
        "## Steps\n\n"
        "- [ ] Step 1\n"
        "- [ ] Step 2\n"
        "- [ ] Step 3\n\n"
        "## Verification\n\n"
        "- [ ] Focused check 1\n"
        "- [ ] Focused check 2\n"
    )


def prd_text(title: str, slug: str, current_date: str) -> str:
    return (
        f"Status: accepted\n"
        f"Mode: prd_backed\n"
        f"Slug: {slug}\n"
        f"Created: {current_date}\n"
        f"Updated: {current_date}\n\n"
        f"# PRD: {title}\n\n"
        "## Problem Statement\n\n"
        "Describe the problem from the user or maintainer perspective.\n\n"
        "## Solution\n\n"
        "Describe the intended solution at the product or system level.\n\n"
        "## User Stories\n\n"
        "1. As a <actor>, I want <capability>, so that <benefit>.\n\n"
        "## Implementation Decisions\n\n"
        "- Durable architectural or interface decisions.\n"
        "- Module ownership and boundary decisions.\n"
        "- Key constraints and clarifications.\n\n"
        "Avoid file paths and volatile implementation snippets.\n\n"
        "## Testing Decisions\n\n"
        "- What makes a good test here.\n"
        "- Which behaviors need focused tests.\n"
        "- What regression coverage should remain.\n\n"
        "## Out of Scope\n\n"
        "- Explicitly excluded work.\n\n"
        "## Further Notes\n\n"
        "- Optional clarifications, dependencies, or migration context.\n"
    )


def prd_backed_plan_text(title: str, slug: str, current_date: str) -> str:
    return (
        f"# Plan: {title}\n\n"
        f"> Status: `in_progress`\n"
        f"> Mode: `prd_backed`\n"
        f"> Progress: `not_started`\n"
        f"> Slug: `{slug}`\n"
        f"> Created: `{current_date}`\n"
        f"> Updated: `{current_date}`\n\n"
        "## Architectural decisions\n\n"
        "Durable decisions that apply across all phases:\n\n"
        "- **Boundary**: ...\n"
        "- **Data model**: ...\n"
        "- **Execution model**: ...\n\n"
        "---\n\n"
        "## Phase 1: Tracer Bullet\n\n"
        "**User stories**: 1\n\n"
        "### What to build\n\n"
        "Describe the end-to-end slice in behavior terms.\n\n"
        "### Acceptance criteria\n\n"
        "- [ ] ...\n"
        "- [ ] ...\n"
    )


def architecture_text(title: str, slug: str, current_date: str) -> str:
    return (
        f"# Architecture: {title}\n\n"
        f"Status: draft\n"
        f"Slug: {slug}\n"
        f"Created: {current_date}\n"
        f"Updated: {current_date}\n\n"
        "## Overview\n\n"
        "Describe the current stable design that should outlive the implementation plan.\n\n"
        "## Key Decisions\n\n"
        "- ...\n\n"
        "## Boundaries\n\n"
        "- ...\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Bootstrap a new Wilco slug with the smallest valid artifact set.")
    parser.add_argument("slug", help="Slug suffix or full dated slug. New slugs default to YYYY-MM-DD-topic form.")
    parser.add_argument("title", help="Human-readable task title.")
    parser.add_argument(
        "--level",
        choices=["no-doc", "plan_only", "prd_backed", "prd_backed_arch"],
        default="plan_only",
        help="Artifact level to create.",
    )
    parser.add_argument("--repo-root", help="Repository root. Defaults to the current working directory.")
    parser.add_argument("--date", default=today_iso(), help="Date to use for Created/Updated metadata.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing target files.")
    parser.add_argument("--no-index", action="store_true", help="Skip creating the initial index manifest.")
    args = parser.parse_args()

    root = repo_root_from_arg(args.repo_root)
    title = args.title
    current_date = args.date
    slug = dated_slug(args.slug, current_date)

    if args.level == "no-doc":
        print(f"No Wilco artifacts created for {slug}: level=no-doc")
        return 0

    ensure_wilco_layout(root)

    targets: list[tuple[Path, str]] = []
    if args.level == "plan_only":
        targets.append((plan_path(root, slug), plan_only_text(title, slug, current_date)))
    else:
        targets.append((prd_path(root, slug), prd_text(title, slug, current_date)))
        targets.append((plan_path(root, slug), prd_backed_plan_text(title, slug, current_date)))
        if args.level == "prd_backed_arch":
            targets.append((architecture_doc_path(root, slug), architecture_text(title, slug, current_date)))

    for path, text in targets:
        write_text(path, text, overwrite=args.force)
        print(f"Wrote {path}")

    if not args.no_index:
        bootstrap_index = {
            "kind": "wilco-linkage-v1",
            "slug": slug,
            "state": {
                "status": "in_progress",
                "progress": "not_started",
                "tracking_mode": "plan_only" if args.level == "plan_only" else "prd_backed",
                "updated": current_date,
            },
            "artifacts": {},
        }
        write_json(index_path(root, slug), bootstrap_index)
        print(f"Wrote {index_path(root, slug)}")
        derived_index = build_index_manifest(root, slug, read_json(index_path(root, slug)))
        if derived_index is not None:
            write_json(index_path(root, slug), derived_index)
            print(f"Derived {index_path(root, slug)}")

    changed = sync_active_headers_for_slug(root, slug, touch_updated=False, current_date=current_date)
    for path in changed:
        print(f"Synced header {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
