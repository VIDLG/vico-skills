# Repository Plan Template

Use this template for `.wilco/plans/active/<slug>.md`.

```md
# Plan: <Feature Name>

> Status: `in_progress`
> Mode: `prd_backed`
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
Treat the checklist as the primary execution anchor; temporary reconcile may validate it later, but does not replace it.
A plan is `wilco-exec` ready only when the next slice can be chosen without guessing, acceptance criteria are observable, and focused verification is named.
If the repository is using index manifests, keep them minimal and derived from the primary docs.
Keep the slug stable once tracked. If the topic truly splits, create a follow-up slug instead of renaming this one, and record the split in both prose and index linkage.
Use this template only for `prd_backed` work. Keep `Mode: prd_backed` explicit in the header.
