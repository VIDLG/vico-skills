---
name: wilco-plan
description: Turn a Wilco-style repo-local PRD into a multi-phase implementation plan using tracer-bullet vertical slices, or create a plan directly for smaller scoped work, then write it under `.wilco/plans/active/`. Use when the user wants to break down a PRD, create an implementation plan from a repository PRD, plan a smaller task without a separate PRD, or keep planning aligned with repository-native docs instead of `./plans/` or issue trackers.
---

# Prd To Repo Plan

## Overview

Convert repository PRDs into active implementation plans that live under `.wilco/plans/active/`. For smaller and clearer tasks, support plan-only work without forcing a separate PRD. Keep the slug stable, capture status and dates in metadata, and prefer vertical slices over horizontal layer-by-layer plans.

The plan is the primary execution document. Its checklist defines the intended path of work and the smallest next executable units.

Before creating anything new, decide whether the work hits an existing active slug. Tiny implementation work can still require plan synchronization when it advances already-tracked work.
Default to plan-only when that is sufficient. A PRD is an escalation, not a baseline requirement.
Do not treat this skill as the normal bootstrap entrypoint for new tracked work. If a new tracked slug does not exist yet, use `wilco-init` first.

## Workflow

1. Determine whether the work hits an existing active slug.
2. If it hits an active slug, update the existing plan instead of creating a sibling slug.
3. If it does not hit an active slug and the work should be tracked, stop and hand off to `wilco-init` instead of minting a new tracked slug here.
4. If it does not hit an active slug and the work should stay `no-doc`, do not create a plan.
5. If PRD-backed, confirm the source PRD path, ideally `.wilco/prd/active/<slug>.md`.
6. If plan-only, confirm the task is small enough that a separate PRD would add more process than clarity.
7. Explore the codebase to understand current architecture, ownership, and integration seams.
8. Identify durable architectural decisions that should apply across all phases.
9. Draft thin vertical slices that produce verifiable behavior end-to-end.
10. Review slice granularity with the user and iterate until approved.
11. Update `.wilco/index/<slug>.json` as a derived machine-readable link to the primary artifacts. Prefer `../wilco-docs/scripts/sync_wilco_index.py` when available instead of hand-editing derived linkage.
12. Write or update the plan at `.wilco/plans/active/<slug>.md` using [references/plan-template.md](references/plan-template.md). Prefer `../wilco-docs/scripts/sync_wilco_headers.py` when header cross-links drift.
13. If there is a source PRD, update the PRD header so `Related plan` points to the new plan path.
14. If implementation reality has diverged materially from the current plan, rewrite the plan to match reality or hand off to `wilco-resume` first if state is unclear.
15. If the repo's docs layout is unclear or drifting, also use `wilco-docs`.

## Planning Rules

- Use one stable topic slug across PRD and plan.
- Keep implementation plans repo-local; do not default to `./plans/`.
- Use tracer-bullet vertical slices, not horizontal batches of layer-specific work.
- Acceptance criteria should describe observable outcomes, not implementation chores.
- Put status and dates in the header so age and freshness remain obvious to humans and agents.
- Do not force a PRD for every task. Small, clear, implementation-facing work can be plan-only.
- Do not create a new plan when the work clearly advances an existing active slug.
- If work hits an existing active slug, do not treat it as `no-doc`; update the plan even for small implementation-facing advances.
- Keep the checklist. The checklist is not redundant with `wilco-resume`; it is the execution anchor that `wilco-execute` should work from.
- Prefer checklist items that are small, behavior-oriented, and verifiable.
- If tracked work advances, even via a tiny "vibe" change, sync the plan checklist and `Updated` date instead of silently relying on code state.
- If scope, goals, or acceptance moved enough that the plan is no longer the right execution contract, update the PRD as well or escalate to `wilco-prd`.
- Treat the plan as the main human-readable execution artifact. The index is supporting metadata, not peer-level prose.

## Sync Contract

- `no-doc` with no slug hit: do not create a plan
- new tracked work with no slug hit: use `wilco-init` first
- existing slug, implementation advance only: update the plan and minimally refresh the index
- existing slug, plan no longer matches implementation: perform `diverge-replan`
- existing slug, task completed: update the plan for completion and coordinate `close-archive` handling with `wilco-docs`

## Output Contract

Write plans with at least:

- `Status`
- optional `Progress`
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
- Use [../wilco-docs/references/automation.md](../wilco-docs/references/automation.md) when syncing derived index metadata.
- Use `wilco-init` when a slug does not exist yet and you need clean initial scaffolding.
- Use `wilco-docs` when you need help with active/archive placement or document lifecycle.
