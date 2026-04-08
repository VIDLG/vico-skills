# Repository PRD Template

Use this template for `.wilco/prd/active/<slug>.md`.

```md
Status: accepted
Slug: <slug>
Created: 2026-04-08
Updated: 2026-04-08
Manifest: optional `.wilco/index/<slug>.json`
Related plan: optional `.wilco/plans/active/<slug>.md`

# PRD: <Feature or Initiative Name>

## Problem Statement

Describe the problem from the user or maintainer perspective.

## Solution

Describe the intended solution at the product or system level.

## User Stories

1. As a <actor>, I want <capability>, so that <benefit>.

## Implementation Decisions

- Durable architectural or interface decisions.
- Module ownership and boundary decisions.
- Key constraints and clarifications.

Avoid file paths and volatile implementation snippets.

## Testing Decisions

- What makes a good test here.
- Which behaviors need focused tests.
- What regression coverage should remain.

## Out of Scope

- Explicitly excluded work.

## Further Notes

- Optional clarifications, dependencies, or migration context.
```

If no machine-readable linkage is needed yet, omit the `Manifest` line entirely.
If this PRD later becomes redundant because the plan fully carries the remaining execution contract, retire it explicitly through `downgrade-to-plan-only`; do not delete it without an archive or retirement trail.
