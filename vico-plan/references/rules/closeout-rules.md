# Close-Out Rules

Delete an active PRD or plan only after explicit user close-out confirmation and when one of these is true. The default close-out action is to delete active docs, not archive them.

- the work is complete
- the work was cancelled
- the document was superseded by a newer active document
- the stable facts were extracted into architecture docs and the original now serves only historical value in git history

## Date Field Guidance

- Use stable slugs in file names; do not rely on dates in file names for ordering.
- `Created`: when the document was first introduced.
- `Updated`: when the document was last materially revised.
- `Completed`: when a plan or PRD stopped being active.
- `Review after` or `Last reviewed`: optional fields for documents that should be revisited on a schedule.

Recommended minimums:

- Active PRD: `Status`, `Created`, `Updated`
- Active plan: `Status`, `Created`, `Updated`
- Close-out notes in durable docs: only when truly needed

## Archive Steps

1. Confirm through `vico-plan verify` or equivalent current-code evidence that the document is no longer an active source of truth.
2. Confirm that the user explicitly asked for close-out in the current turn.
3. Extract any still-relevant facts into architecture docs.
4. Record any important `Outcome`, `Deviations`, or `Follow-up` notes elsewhere if they still matter.
5. Delete the active file through the repo-local lifecycle surface such as `vico-ops close` or `vico-ops cancel`.
6. Remove stale temporary reconcile snapshots and delete the index once no active artifact set remains.

## Completion Summary Template

```md
## Outcome
- What shipped
- What did not ship

## Deviations
- Important differences from the plan or PRD

## Follow-up
- Remaining work that belongs elsewhere
```

## Anti-Patterns

- treating `verify` as if it automatically performs close-out deletion
- deleting active docs just because an agent believes the work is complete
- leaving a completed plan in an active directory without either a clear pending-manual-close state or a justified reason to keep it active
- relying on deleted PRD content in memory instead of extracting needed truth into architecture docs
- treating `.vico/resume/` as a history store instead of a current-state handoff location
- treating `.vico/index/` as if it were the primary source of scope or execution truth
- performing close-out deletion as if it were the same lifecycle stage as active execution
