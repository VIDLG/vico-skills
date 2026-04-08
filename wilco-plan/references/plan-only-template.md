# Plan-Only Template

Use this template for smaller scoped work that does not justify a separate PRD.

```md
# Plan: <Task Name>

> Status: `in_progress`
> Slug: `<slug>`
> Manifest: `.wilco/index/<slug>.json`
> Created: `2026-04-08`
> Updated: `2026-04-08`

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
Treat the checklist as the execution anchor; `wilco-resume` exists to verify the real state against it.
