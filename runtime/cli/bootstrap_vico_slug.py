#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.vico_artifacts.vico_common import (  # noqa: E402
    architecture_doc_path,
    build_index_manifest,
    ensure_vico_layout,
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
CODE_BLOCK_RE = re.compile(r"```md\n(?P<body>[\s\S]*?)\n```")


def dated_slug(raw_slug: str, current_date: str) -> str:
    slug = raw_slug.strip()
    if DATED_SLUG_RE.match(slug):
        return slug
    return f"{current_date}-{slug}"


def template_body(relative_path: str) -> str:
    path = ROOT / "vico-plan" / "references" / "templates" / relative_path
    text = path.read_text(encoding="utf-8")
    match = CODE_BLOCK_RE.search(text)
    if not match:
        raise SystemExit(f"Template code block not found in {path}")
    return match.group("body").strip() + "\n"


def render_template(body: str, replacements: dict[str, str], *, drop_optional_prefixes: tuple[str, ...] = ()) -> str:
    for key, value in replacements.items():
        body = body.replace(key, value)
    if drop_optional_prefixes:
        kept: list[str] = []
        for line in body.splitlines():
            if any(line.startswith(prefix) for prefix in drop_optional_prefixes):
                continue
            kept.append(line)
        body = "\n".join(kept)
    return body.strip() + "\n"


def plan_only_text(title: str, slug: str, current_date: str) -> str:
    body = template_body("plan-only-template.md")
    return render_template(
        body,
        {
            "<Task Name>": title,
            "<slug>": slug,
            "optional `partially_completed`": "`not_started`",
            "2026-04-08": current_date,
        },
        drop_optional_prefixes=("> Manifest:",),
    )


def prd_text(title: str, slug: str, current_date: str) -> str:
    body = template_body("prd-template.md")
    return render_template(
        body,
        {
            "<Feature or Initiative Name>": title,
            "<slug>": slug,
            "2026-04-08": current_date,
            "Execution Plan: optional `.vico/plans/active/<slug>.md`": f"Execution Plan: `.vico/plans/active/{slug}.md`",
        },
        drop_optional_prefixes=("Manifest:",),
    )


def prd_backed_plan_text(title: str, slug: str, current_date: str) -> str:
    body = template_body("plan-template.md")
    return render_template(
        body,
        {
            "<Feature Name>": title,
            "<slug>": slug,
            "optional `partially_completed`": "`not_started`",
            "2026-04-08": current_date,
            "## Phase 1: <Title>": "## Phase 1: Tracer Bullet",
            "**User stories**: 1, 3, 4": "**User stories**: 1",
            "### Acceptance criteria\n\n- [ ] ...\n- [ ] ...\n\nChecklist items should describe observable completion, not vague implementation churn.\n\n---\n\n## Phase 2: <Title>\n\n**User stories**: ...\n\n### What to build\n\n...\n\n### Acceptance criteria\n\n- [ ] ...": "### Acceptance criteria\n\n- [ ] ...\n- [ ] ...",
            "> Source PRD: `.vico/prd/active/<slug>.md`": f"> Source PRD: `.vico/prd/active/{slug}.md`",
        },
        drop_optional_prefixes=("> Manifest:",),
    )


def architecture_text(title: str, slug: str, current_date: str) -> str:
    body = template_body("architecture-template.md")
    return render_template(
        body,
        {
            "<Feature or Initiative Name>": title,
            "<slug>": slug,
            "2026-04-08": current_date,
        },
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Bootstrap a new Vico slug with the smallest valid artifact set.")
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
        print(f"No Vico artifacts created for {slug}: level=no-doc")
        return 0

    ensure_vico_layout(root)

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
            "kind": "vico-linkage-v1",
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
