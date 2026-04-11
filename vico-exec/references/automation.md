# Vico Exec Automation

Use automation to reduce repeatable index maintenance during execution.

## Sync Derived Index

Use `scripts/sync_vico_index.py` to rebuild `.vico/index/*.json` from the current active plan, PRD, resume, and architecture docs.

Examples:

```bash
python3 vico-skills/vico-exec/scripts/sync_vico_index.py --repo-root D:/projects/spoon
python3 vico-skills/vico-exec/scripts/sync_vico_index.py architecture-cleanup --repo-root D:/projects/spoon
python3 vico-skills/vico-exec/scripts/sync_vico_index.py --repo-root D:/projects/spoon --prune --dry-run
```

Use it after:

- updating temporary reconcile linkage
- clearing stale temporary reconcile files
- normalizing architecture links
- repairing missing derived linkage for an already-tracked slug

Treat this as execution-stage linkage maintenance, not as a substitute for `vico-plan` bootstrap or close-out workflows.
