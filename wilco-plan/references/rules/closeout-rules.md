# Close-Out Rules

Delete an active PRD or plan when one of these is true. The default close-out action is to delete active docs, not archive them.

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

1. Confirm through `wilco-plan verify` or equivalent current-code evidence that the document is no longer an active source of truth.
2. Extract any still-relevant facts into architecture docs.
3. Record any important `Outcome`, `Deviations`, or `Follow-up` notes elsewhere if they still matter.
4. Delete the active file.
5. Remove stale temporary reconcile snapshots and delete the index once no active artifact set remains.

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
- leaving a completed plan in an active directory without deleting it
- relying on deleted PRD content in memory instead of extracting needed truth into architecture docs
- treating `.wilco/resume/` as a history store instead of a current-state handoff location
- treating `.wilco/index/` as if it were the primary source of scope or execution truth
- performing close-out deletion as if it were the same lifecycle stage as active execution
