# Vico Automation

Use automation to reduce repeatable Vico maintenance work.

## Bootstrap A New Slug

Use `vico-ops bootstrap` for the repo-local maintenance surface, backed by `runtime/cli/bootstrap_vico_slug.py`.

Examples:

```bash
python vico-skills/vico-plan/scripts/bootstrap_vico_slug.py tiny-fix "Tiny Fix" --repo-root D:/projects/spoon
python vico-skills/vico-plan/scripts/bootstrap_vico_slug.py boundary-work "Boundary Work" --repo-root D:/projects/spoon --level prd_backed_arch
```

These commands assume a repository checkout or copied local utility path.
Owner sources live under `runtime/cli/`; `vico-plan/scripts/` remains the compatibility command path.

Use it when:

- a task first enters `.vico`
- you want consistent initial plan/PRD headers
- you want the starter index for a tracked slug without hand-writing JSON

## Sync Active Headers

Use `vico-ops sync` to repair plan and PRD headers after moves, new manifests, or cross-link drift.

Examples:

```bash
python vico-skills/vico-plan/scripts/sync_vico_headers.py --repo-root D:/projects/spoon
python vico-skills/vico-plan/scripts/sync_vico_headers.py architecture-cleanup --repo-root D:/projects/spoon --touch-updated
```

Use it after:

- creating a new slug
- restoring or deleting index manifests
- moving between `plan_only` and `prd_backed` tracking
- fixing stale `Manifest`, `Source PRD`, or `Execution Plan` lines

## Validate The Workspace

Use `vico-ops validate` to validate the current `.vico` workspace against the Vico schema.

Examples:

```bash
python vico-skills/vico-plan/scripts/validate_vico_workspace.py --repo-root D:/projects/spoon
```

Use it after:

- large doc rewrites
- migration to the new status vocabulary
- scripted cleanup or bootstrap flows
- before trusting `.vico` as an execution source of truth

## Sync Derived Index

Use `vico-ops sync` to rebuild `.vico/index/*.json` from the current active plan, PRD, resume, and architecture docs when derived state must catch up.

Examples:

```bash
python vico-skills/vico-plan/scripts/sync_vico_index.py --repo-root D:/projects/spoon
python vico-skills/vico-plan/scripts/sync_vico_index.py architecture-cleanup --repo-root D:/projects/spoon
python vico-skills/vico-plan/scripts/sync_vico_index.py --repo-root D:/projects/spoon --prune --dry-run
```

Use it after:

- creating or renaming active artifacts
- updating temporary reconcile linkage
- clearing stale temporary reconcile files
- normalizing architecture links
- repairing missing derived linkage for an already-tracked slug

## Close And Archive A Slug

Use `vico-ops close` or `vico-ops cancel` to delete active plan and PRD files, clean temporary resume state, and remove index linkage.

Examples:

```bash
python vico-skills/vico-plan/scripts/close_vico_slug.py architecture-cleanup --repo-root D:/projects/spoon --dry-run
python vico-skills/vico-plan/scripts/close_vico_slug.py architecture-cleanup --repo-root D:/projects/spoon
```

Default behavior:

- delete active plan
- delete active PRD
- delete the current temporary reconcile file unless asked to keep it
- delete the current index file
Treat this as cleanup-stage automation, not as the normal terminal step inside `vico-exec`.
