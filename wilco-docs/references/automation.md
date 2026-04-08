# Wilco Automation

Use automation to reduce repeatable Wilco maintenance work.

## Bootstrap A New Slug

Use `../wilco-init/scripts/bootstrap_wilco_slug.py` to create the smallest valid initial artifact set for new tracked work.

Examples:

```bash
python3 wilco-skills/wilco-init/scripts/bootstrap_wilco_slug.py tiny-fix "Tiny Fix" --repo-root D:/projects/spoon
python3 wilco-skills/wilco-init/scripts/bootstrap_wilco_slug.py boundary-work "Boundary Work" --repo-root D:/projects/spoon --level prd-plan-arch
```

Use it when:

- a task first enters `.wilco`
- you want consistent initial plan/PRD headers
- you want the starter index for a tracked slug without hand-writing JSON

## Sync Active Headers

Use `scripts/sync_wilco_headers.py` to repair plan and PRD headers after moves, new manifests, or cross-link drift.

Examples:

```bash
python3 wilco-skills/wilco-docs/scripts/sync_wilco_headers.py --repo-root D:/projects/spoon
python3 wilco-skills/wilco-docs/scripts/sync_wilco_headers.py architecture-cleanup --repo-root D:/projects/spoon --touch-updated
```

Use it after:

- creating a new slug
- restoring or deleting index manifests
- moving between plan-only and PRD-backed tracking
- fixing stale `Manifest`, `Source PRD`, or `Related plan` lines

## Validate The Workspace

Use `scripts/validate_wilco_workspace.py` to validate the current `.wilco` workspace against the Wilco schema.

Examples:

```bash
python3 wilco-skills/wilco-docs/scripts/validate_wilco_workspace.py --repo-root D:/projects/spoon
```

Use it after:

- large doc rewrites
- migration to the new status vocabulary
- scripted cleanup or bootstrap flows
- before trusting `.wilco` as an execution source of truth

## Sync Derived Index

Use `scripts/sync_wilco_index.py` to rebuild `.wilco/index/*.json` from the current active plan, PRD, resume, and architecture docs.

Examples:

```bash
python3 wilco-skills/wilco-docs/scripts/sync_wilco_index.py --repo-root D:/projects/spoon
python3 wilco-skills/wilco-docs/scripts/sync_wilco_index.py architecture-cleanup --repo-root D:/projects/spoon
python3 wilco-skills/wilco-docs/scripts/sync_wilco_index.py --repo-root D:/projects/spoon --prune --dry-run
```

Use it after:

- creating or renaming active artifacts
- updating resume linkage
- clearing stale resume files
- normalizing architecture links
- repairing missing derived linkage for an already-tracked slug

## Close And Archive A Slug

Use `scripts/close_wilco_slug.py` to archive active plan and PRD files, clean temporary resume state, and remove or rewrite index linkage.

Examples:

```bash
python3 wilco-skills/wilco-docs/scripts/close_wilco_slug.py architecture-cleanup --repo-root D:/projects/spoon --dry-run
python3 wilco-skills/wilco-docs/scripts/close_wilco_slug.py architecture-cleanup --repo-root D:/projects/spoon
```

Default behavior:

- move active plan to `.wilco/plans/archive/`
- move active PRD to `.wilco/prd/archive/`
- stamp `Status: archived`, `Updated`, and `Completed`
- delete the current resume file unless asked to keep it
- delete the current index file unless asked to keep an archived manifest

Use `--keep-index` only when you intentionally want archived linkage metadata to survive.
Treat this as cleanup-stage automation, not as the normal terminal step inside `wilco-execute`.
