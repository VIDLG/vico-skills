---
name: wilco-cleanup
description: Close completed or abandoned Wilco slugs by archiving active plan and PRD files, clearing temporary resume and index state, and tidying stale Wilco artifacts. Use when the work is effectively done, when active docs should move to archive, when stale resume or index linkage should be removed, or when the user asks to clean up `.wilco` after execution or reconciliation.
---

# Wilco Cleanup

## Overview

Close out a Wilco slug once active execution is no longer the main concern. Keep cleanup narrow: archive finished planning docs, remove temporary handoff state, and leave durable truth in architecture docs.

This skill is for close-out and hygiene work, not for deciding what the truth is. If `.wilco` and code disagree, run `wilco-resume` first and come back with a verified current state.
Users should not need to remember this skill manually after a successful execution run. Agents may route here automatically once implementation is verified done.

## Workflow

1. Confirm the slug and whether the work is:
   - complete
   - cancelled
   - superseded
   - or just carrying stale temporary state
2. If current truth is unclear, stop and use `wilco-resume` first.
3. Confirm any durable facts that still belong in `docs/architecture/`.
4. Archive active plan and PRD files when they are no longer active sources of truth.
5. Delete temporary resume state unless a live handoff still needs it.
6. Remove stale or unnecessary index linkage, or rewrite it only when archived linkage is intentionally desired.
7. Leave active directories small and unambiguous.

## Decision Rules

- If the slug is still actively being implemented, do not use this skill yet.
- If the slug is done and the plan or PRD still sits under `active/`, archive it.
- If a resume file exists only because of an old handoff, delete it.
- If an index file only mirrors stale paths, rebuild or delete it instead of hand-editing ad hoc JSON.
- If architecture truth is still trapped only in PRD or plan text, extract it before archiving.

## Automation

Prefer the bundled automation from `wilco-docs`:

- `../wilco-docs/scripts/close_wilco_slug.py` for normal close-out and archive handling
- `../wilco-docs/scripts/sync_wilco_headers.py` if archive cross-links or manifest lines need repair first
- `../wilco-docs/scripts/sync_wilco_index.py` for derived index refresh after cleanup or resume deletion

Use dry-run first when the slug is important or the cleanup scope is unclear.

## References

- Use [references/close-checklist.md](references/close-checklist.md) before archive or deletion work.
- Use [references/cleanup-output-template.md](references/cleanup-output-template.md) for structured cleanup reports.
- Use [../wilco-docs/references/archive.md](../wilco-docs/references/archive.md) for archive status blocks and completion handling.
- Use [../wilco-docs/references/automation.md](../wilco-docs/references/automation.md) for scripted cleanup flows.
- Use [../wilco-docs/references/troubleshooting.md](../wilco-docs/references/troubleshooting.md) when you are not sure whether cleanup is actually the next step.
