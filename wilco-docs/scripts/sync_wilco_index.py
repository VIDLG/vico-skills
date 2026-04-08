#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from wilco_common import active_slugs, build_index_manifest, index_path, read_json, repo_root_from_arg, write_json


def main() -> int:
    parser = argparse.ArgumentParser(description="Derive minimal .wilco/index manifests from current Wilco artifacts.")
    parser.add_argument("slugs", nargs="*", help="Optional slugs to sync. Defaults to all active slugs and existing index entries.")
    parser.add_argument("--repo-root", help="Repository root. Defaults to the current working directory.")
    parser.add_argument("--dry-run", action="store_true", help="Print planned changes without writing files.")
    parser.add_argument("--prune", action="store_true", help="Delete stale index files that have no active plan, PRD, or resume.")
    args = parser.parse_args()

    root = repo_root_from_arg(args.repo_root)
    slugs = sorted(set(args.slugs) if args.slugs else active_slugs(root))
    if not slugs:
        print("No Wilco slugs found.")
        return 0

    for slug in slugs:
        path = index_path(root, slug)
        existing = read_json(path)
        manifest = build_index_manifest(root, slug, existing)

        if manifest is None:
            if path.exists() and args.prune:
                if args.dry_run:
                    print(f"[dry-run] prune {path}")
                else:
                    path.unlink()
                    print(f"Pruned {path}")
            else:
                print(f"Skipped {slug}: no active plan, PRD, or resume.")
            continue

        rendered = json.dumps(manifest, indent=2, ensure_ascii=True) + "\n"
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current == rendered:
            print(f"Up to date: {path}")
            continue

        if args.dry_run:
            print(f"[dry-run] write {path}")
            print(rendered.rstrip())
        else:
            write_json(path, manifest)
            print(f"Wrote {path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
