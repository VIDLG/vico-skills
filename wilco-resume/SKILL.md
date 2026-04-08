---
name: wilco-resume
description: Reconcile Wilco PRDs, plans, and current code or test state to determine real progress and the correct next step. Use when implementation was interrupted, the user asks how to continue, wants to compare current code against a PRD or plan, needs to verify what is actually done, or wants a resume report before continuing work. Also use when a task has only a plan and code state, without a separate PRD.
---

# Wilco Resume

## Overview

Reconstruct the true state of work by comparing three sources of truth:

- the PRD
- the plan
- the current code and tests

When no PRD exists because the task was intentionally plan-only, reconcile the plan against code and tests without treating the missing PRD as an error.

Do not trust checklist state alone. Verify implementation reality in code and tests before concluding that a phase is done, partial, diverged, or still pending.

## Workflow

1. Locate the target plan, and locate the PRD if one exists.
   Prefer:
   - `.wilco/plans/active/<slug>.md`
   - `.wilco/prd/active/<slug>.md`
2. Determine whether this is:
   - PRD + plan + code reconciliation
   - or plan + code reconciliation
3. If a PRD exists, read it to recover scope, intended outcomes, constraints, and out-of-scope boundaries.
4. Read the plan to recover phases, acceptance criteria, architectural decisions, and current documented status.
5. Explore the codebase and tests for evidence of completion, partial completion, divergence, or abandoned work.
6. Reconcile the available docs and implementation into a resume report.
7. Recommend the smallest correct next step.
8. If the docs are stale, recommend whether to update:
   - the plan
   - the PRD, if one exists or is actually needed
   - architecture docs
   Do not rewrite them automatically unless the user asks.

## Reconciliation Rules

- Do not mark work as done unless the code or tests support that conclusion.
- Distinguish `done`, `partial`, `not_started`, `diverged`, and `unclear`.
- Treat deleted legacy paths, compatibility shims, and renamed modules as evidence that the plan may be stale even if behavior exists.
- Prefer public behavior and preserved tests over internal implementation shape.
- If the implementation changed direction but still satisfies the PRD, record that as plan divergence, not automatic failure.
- If the plan references paths or architecture that no longer exist, call that out explicitly.

## Output Contract

Produce a resume report that includes:

- current PRD status
- current plan status
- overall implementation status
- phase-by-phase verification
- divergences between PRD, plan, and code
- unresolved decisions or unclear areas
- the recommended next step
- recommended doc updates, if any

## References

- Use [references/resume-checklist.md](references/resume-checklist.md) for what evidence to inspect.
- Use [references/resume-output-template.md](references/resume-output-template.md) for the report format.

If the reconciliation shows the document lifecycle itself is unclear, also use `wilco-docs`.
