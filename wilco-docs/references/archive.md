# Archive Rules

Archive a PRD or plan when one of these is true:

- the work is complete
- the work was cancelled
- the document was superseded by a newer document
- the stable facts were extracted into architecture docs and the original now serves only historical value

## Status Block Template

Use an explicit header near the top of archived documents:

```md
Status: archived
Created: 2026-04-08
Updated: 2026-04-20
Completed: 2026-04-20
Slug: action-pipeline
Current architecture: docs/architecture/action-pipeline.md
Superseded by: .wilco/plans/archive/action-pipeline-v2.md
```

Only include fields that are actually known. `Current architecture` and `Superseded by` are optional.

## Date Field Guidance

- Use stable slugs in file names; do not rely on dates in file names for ordering.
- `Created`: when the document was first introduced.
- `Updated`: when the document was last materially revised.
- `Completed`: when a plan or PRD stopped being active.
- `Review after` or `Last reviewed`: optional fields for documents that should be revisited on a schedule.

Recommended minimums:

- Active PRD: `Status`, `Created`, `Updated`
- Active plan: `Status`, `Created`, `Updated`
- Archived plan/PRD: `Status`, `Created`, `Updated`, `Completed`

## Archive Steps

1. Confirm the document is no longer an active source of truth.
2. Extract any still-relevant facts into architecture docs.
3. Move the file into the correct archive directory.
4. Add or update the status block.
5. Add an `Outcome`, `Deviations`, or `Follow-up` section if the implementation materially differed from the original document.

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

- leaving a completed plan in an active directory without status updates
- relying on an archived PRD as the only place where current architecture is documented
- moving files into archive without replacement links when a current document exists
