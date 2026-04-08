# Close Checklist

Use this checklist before closing a Wilco slug.

## Preconditions

- The implementation is complete, cancelled, or clearly superseded.
- The current state is verified. If not, run `wilco-resume` first.
- The slug is no longer the main active execution target.

## Checklist

- [ ] Active plan is no longer needed under `.wilco/plans/active/`
- [ ] Active PRD is no longer needed under `.wilco/prd/active/`
- [ ] Any durable facts needed later live in `docs/architecture/` or an ADR
- [ ] Temporary resume state is either still needed for a live handoff or can be deleted
- [ ] Index linkage will be deleted or intentionally preserved in archived form
- [ ] Archive metadata will include `Status`, `Updated`, and `Completed`
- [ ] Any important deviations or follow-up items are recorded before archive

## Default Close-Out

For the normal finished-work case:

1. archive the active plan
2. archive the active PRD if one exists
3. delete the temporary resume file
4. delete the active index manifest
5. leave durable truth in architecture docs

## When Not To Close

Do not close the slug yet when:

- another implementation slice is still planned and active
- the current code and docs disagree in a material way
- the resume file is still serving a live handoff
- important architecture truth has not been extracted yet
