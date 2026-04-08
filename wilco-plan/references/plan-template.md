# Repository Plan Template

Use this template for `.wilco/plans/active/<slug>.md`.

```md
# Plan: <Feature Name>

> Status: `in_progress`
> Progress: optional `partially_completed`
> Slug: `<slug>`
> Created: `2026-04-08`
> Updated: `2026-04-08`
> Manifest: optional `.wilco/index/<slug>.json`
> Source PRD: `.wilco/prd/active/<slug>.md`

## Architectural decisions

Durable decisions that apply across all phases:

- **Boundary**: ...
- **Data model**: ...
- **Execution model**: ...

---

## Phase 1: <Title>

**User stories**: 1, 3, 4

### What to build

Describe the end-to-end slice in behavior terms.

### Acceptance criteria

- [ ] ...
- [ ] ...

Checklist items should describe observable completion, not vague implementation churn.

---

## Phase 2: <Title>

**User stories**: ...

### What to build

...

### Acceptance criteria

- [ ] ...
```

Prefer many thin slices over a few thick ones. Each phase should be demoable or verifiable on its own.
Treat the checklist as the primary execution anchor; later `wilco-resume` output validates it, but does not replace it.
If the repository is using index manifests, keep them minimal and derived from the primary docs.
Keep the slug stable once tracked. If the topic truly splits, create a follow-up slug instead of renaming this one, and record the split in both prose and index linkage.
If an active PRD is retired through `downgrade-to-plan-only`, remove the `Source PRD` line and make this plan the sole active execution contract.
