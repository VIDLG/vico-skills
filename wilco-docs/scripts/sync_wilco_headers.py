#!/usr/bin/env python3
from __future__ import annotations

import argparse

from wilco_common import active_slugs, repo_root_from_arg, sync_active_headers_for_slug, today_iso


def main() -> int:
    parser = argparse.ArgumentParser(description="Synchronize Wilco plan/PRD headers with current slug, cross-links, and manifest paths.")
    parser.add_argument("slugs", nargs="*", help="Optional slugs to sync. Defaults to all active slugs.")
    parser.add_argument("--repo-root", help="Repository root. Defaults to the current working directory.")
    parser.add_argument("--touch-updated", action="store_true", help="Refresh Updated dates to today while syncing headers.")
    parser.add_argument("--date", default=today_iso(), help="Date to use when filling missing Created/Updated metadata.")
    args = parser.parse_args()

    root = repo_root_from_arg(args.repo_root)
    slugs = sorted(set(args.slugs) if args.slugs else active_slugs(root))
    if not slugs:
        print("No Wilco slugs found.")
        return 0

    for slug in slugs:
        changed = sync_active_headers_for_slug(root, slug, touch_updated=args.touch_updated, current_date=args.date)
        if changed:
            for path in changed:
                print(f"Updated {path}")
        else:
            print(f"Up to date: {slug}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
