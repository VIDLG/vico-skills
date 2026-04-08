# Repository Plan Template

Use this template for `.wilco/plans/active/<slug>.md`.

```md
# Plan: <Feature Name>

> Status: `in_progress`
> Slug: `<slug>`
> Manifest: `.wilco/index/<slug>.json`
> Created: `2026-04-08`
> Updated: `2026-04-08`
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
