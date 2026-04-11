# Repository PRD Template

Use this template for internal `prd_backed` upgrades under `.wilco/prd/active/<slug>.md`.

```md
Status: accepted
Mode: prd_backed
Slug: <slug>
Created: 2026-04-08
Updated: 2026-04-08
Manifest: optional `.wilco/index/<slug>.json`
Execution Plan: optional `.wilco/plans/active/<slug>.md`

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

Use this template only for `prd_backed` slugs. Do not create a PRD when the active plan already carries enough context.
