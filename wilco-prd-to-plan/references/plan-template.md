# Repository Plan Template

Use this template for `docs/plans/active/<slug>.md`.

```md
# Plan: <Feature Name>

> Status: `in_progress`
> Created: `2026-04-08`
> Updated: `2026-04-08`
> Source PRD: `docs/prd/active/<slug>.md`

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

---

## Phase 2: <Title>

**User stories**: ...

### What to build

...

### Acceptance criteria

- [ ] ...
```

Prefer many thin slices over a few thick ones. Each phase should be demoable or verifiable on its own.
