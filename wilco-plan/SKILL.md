---
name: wilco-plan
description: Turn a Wilco-style repo-local PRD into a multi-phase implementation plan using tracer-bullet vertical slices, or create a plan directly for smaller scoped work, then write it to `.wilco/plans/active/<slug>.md`. Use when the user wants to break down a PRD, create an implementation plan from a repository PRD, plan a smaller task without a separate PRD, or keep planning aligned with repository-native docs instead of `./plans/` or issue trackers.
---

# Prd To Repo Plan

## Overview

Convert repository PRDs into active implementation plans that live under `.wilco/plans/active/`. For smaller and clearer tasks, support plan-only work without forcing a separate PRD. Keep the slug stable, capture status and dates in metadata, and prefer vertical slices over horizontal layer-by-layer plans.

The plan is the primary execution document. Its checklist defines the intended path of work and the smallest next executable units.

## Workflow

1. Determine whether this plan is PRD-backed or plan-only.
2. If PRD-backed, confirm the source PRD path, ideally `.wilco/prd/active/<slug>.md`.
3. If plan-only, confirm the task is small enough that a separate PRD would add more process than clarity.
4. If `.wilco/` does not exist yet, initialize it as the Wilco planning workspace before writing any plan files.
5. Explore the codebase to understand current architecture, ownership, and integration seams.
6. Identify durable architectural decisions that should apply across all phases.
7. Draft thin vertical slices that produce verifiable behavior end-to-end.
8. Review slice granularity with the user and iterate until approved.
9. Create or update `.wilco/index/<slug>.json` so the active plan has a machine-readable link to its PRD, resume snapshot, and related architecture docs.
10. Write the plan to `.wilco/plans/active/<slug>.md` using [references/plan-template.md](references/plan-template.md).
11. If there is a source PRD, update the PRD header so `Related plan` points to the new plan path.
12. If the repo's docs layout is unclear or drifting, also use `wilco-docs`.

## Planning Rules

- Use one stable topic slug across PRD and plan.
- Keep implementation plans repo-local; do not default to `./plans/`.
- Use tracer-bullet vertical slices, not horizontal batches of layer-specific work.
- Acceptance criteria should describe observable outcomes, not implementation chores.
- Put status and dates in the header so age and freshness remain obvious to humans and agents.
- Do not force a PRD for every task. Small, clear, implementation-facing work can be plan-only.
- Keep the checklist. The checklist is not redundant with `wilco-resume`; it is the execution anchor that `wilco-execute` should work from.
- Prefer checklist items that are small, behavior-oriented, and verifiable.

## Output Contract

Write plans with at least:

- `Status`
- `Created`
- `Updated`
- optional `Source PRD`
- architectural decisions section
- phased slices
- acceptance criteria per phase

Use the full phased template for medium and large work. For small plan-only work, use the lighter plan-only template.

## References

- Use [references/plan-template.md](references/plan-template.md) for the repository plan template.
- Use [references/plan-only-template.md](references/plan-only-template.md) for smaller plan-only work.
- Use `.wilco/index/<slug>.json` as the machine-readable linkage file for cross-agent coordination.
- Use [../wilco-docs/references/status-vocabulary.md](../wilco-docs/references/status-vocabulary.md) when expressing progress or divergence.
- Use `wilco-docs` when you need help with active/archive placement or document lifecycle.
