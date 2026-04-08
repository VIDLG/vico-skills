---
name: wilco-plan
description: Turn a Wilco-style repo-local PRD into a multi-phase implementation plan using tracer-bullet vertical slices, then write it to `docs/plans/active/<slug>.md`. Use when the user wants to break down a PRD, create an implementation plan from a repository PRD, plan phases from `docs/prd/active/`, or keep planning aligned with repository-native docs instead of `./plans/` or GitHub issues.
---

# Prd To Repo Plan

## Overview

Convert repository PRDs into active implementation plans that live under `docs/plans/active/`. Keep the slug stable, capture status and dates in metadata, and prefer vertical slices over horizontal layer-by-layer plans.

## Workflow

1. Confirm the source PRD path, ideally `docs/prd/active/<slug>.md`.
2. Explore the codebase to understand current architecture, ownership, and integration seams.
3. Identify durable architectural decisions that should apply across all phases.
4. Draft thin vertical slices that produce verifiable behavior end-to-end.
5. Review slice granularity with the user and iterate until approved.
6. Write the plan to `docs/plans/active/<slug>.md` using [references/plan-template.md](references/plan-template.md).
7. If needed, update the PRD header so `Related plan` points to the new plan path.
8. If the repo's docs layout is unclear or drifting, also use `wilco-docs`.

## Planning Rules

- Use one stable topic slug across PRD and plan.
- Keep implementation plans repo-local; do not default to `./plans/`.
- Use tracer-bullet vertical slices, not horizontal batches of layer-specific work.
- Acceptance criteria should describe observable outcomes, not implementation chores.
- Put status and dates in the header so age and freshness remain obvious to humans and agents.

## Output Contract

Write plans with at least:

- `Status`
- `Created`
- `Updated`
- `Source PRD`
- architectural decisions section
- phased slices
- acceptance criteria per phase

## References

- Use [references/plan-template.md](references/plan-template.md) for the repository plan template.
- Use `wilco-docs` when you need help with active/archive placement or document lifecycle.
