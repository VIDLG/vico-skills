# Plan-Only Template

Use this template for smaller scoped work that does not justify a separate PRD.

```md
# Plan: <Task Name>

> Status: `in_progress`
> Mode: `plan_only`
> Progress: optional `partially_completed`
> Slug: `<slug>`
> Created: `2026-04-08`
> Updated: `2026-04-08`
> Manifest: optional `.vico/index/<slug>.json`

## Goal

Describe the concrete task outcome in one short paragraph.

## Constraints

- ...

## Steps

- [ ] Step 1
- [ ] Step 2
- [ ] Step 3

## Verification

- [ ] Focused check 1
- [ ] Focused check 2
```

Prefer this template when a PRD would mostly restate the same information in longer form.
Treat the checklist as the execution anchor; temporary reconcile may verify the real state against it when needed.
A plan is `vico-exec` ready only when the next slice can be chosen without guessing, verification is focused, and unresolved user decisions are explicit.
If no machine-readable linkage is needed yet, omit the `Manifest` line entirely.
Keep the slug stable once tracked. If the work later splits into a new topic, create a follow-up slug instead of renaming this one, and record the split in prose plus index linkage.
Use this template for the default `plan_only` mode. It should carry both intent and execution.
