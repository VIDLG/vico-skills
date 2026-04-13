# Vico Exec Automation

Use automation to reduce repeatable index maintenance during execution.

## Claude Runner Loop

Use `scripts/claude_exec_runner.py` when Claude Code should keep executing and verifying until it reaches a real stop condition.

Examples:

```bash
python vico-skills/vico-exec/scripts/claude_exec_runner.py --repo-root D:/projects/spoon
python vico-skills/vico-exec/scripts/claude_exec_runner.py --repo-root D:/projects/spoon --slug 2026-04-12-example --max-iterations 20
python vico-skills/vico-exec/scripts/claude_exec_runner.py --repo-root D:/projects/spoon --permission-mode acceptEdits --effort high
```

These commands assume a repository checkout or copied local utility path.

Use it when:

- hooks are too weak to keep Claude Code in the loop
- the plan is already active and execution should persist
- you want structured `continue` / `done` / `blocked` / `needs_user` / `stale_plan` loop control

Treat the runner as an execution wrapper around `vico-exec`, not as a replacement for `vico-plan`.

## Sync Derived Index

Use `scripts/sync_vico_index.py` to rebuild `.vico/index/*.json` from the current active plan, PRD, resume, and architecture docs.

Examples:

```bash
python vico-skills/vico-exec/scripts/sync_vico_index.py --repo-root D:/projects/spoon
python vico-skills/vico-exec/scripts/sync_vico_index.py architecture-cleanup --repo-root D:/projects/spoon
python vico-skills/vico-exec/scripts/sync_vico_index.py --repo-root D:/projects/spoon --prune --dry-run
```

Use it after:

- updating temporary reconcile linkage
- clearing stale temporary reconcile files
- normalizing architecture links
- repairing missing derived linkage for an already-tracked slug

Treat this as execution-stage linkage maintenance, not as a substitute for `vico-plan` bootstrap or close-out workflows.
