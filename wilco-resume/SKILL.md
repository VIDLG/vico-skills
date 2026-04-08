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

`wilco-resume` does not replace the plan. It audits the plan against implementation reality, records the current handoff state, and tells the next executor where to continue.

## Workflow

1. If `.wilco/` does not exist yet, stop and explain that Wilco planning artifacts have not been initialized for this repository yet.
2. Prefer `.wilco/index/<slug>.json` as the primary coordination entrypoint when it exists.
3. From the index, resolve the current linked PRD, plan, and resume paths.
4. If no index exists yet, fall back to locating the target plan, and the PRD if one exists.
3. Determine whether this is:
   - PRD + plan + code reconciliation
   - or plan + code reconciliation
4. If a PRD exists, read it to recover scope, intended outcomes, constraints, and out-of-scope boundaries.
5. Read the plan to recover phases, acceptance criteria, architectural decisions, and current documented status.
6. Explore the codebase and tests for evidence of completion, partial completion, divergence, or abandoned work.
7. Decide whether any existing resume file is stale enough that it must be replaced.
8. Reconcile the available docs and implementation into a resume report.
9. Write or overwrite the current handoff file at `.wilco/resume/<slug>.md`.
10. If `.wilco/index/<slug>.json` exists, update `state.updated` and `artifacts.resume_current` so later agents can find the current handoff artifact quickly.
11. Recommend the smallest correct next step.
12. If the docs are stale, recommend whether to update:
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
- Record evidence explicitly enough that another reader can see why the conclusion is `high`, `medium`, or `low` confidence.
- Treat the plan checklist as the intended execution path and the resume report as the verified current-state snapshot.
- Treat an existing resume file as stale when the linked PRD or plan has a newer update, when checklist state materially changed, or when current code and tests clearly exceed the old resume conclusions.

## Output Contract

Produce a resume report that includes:

- current PRD status
- current plan status
- alignment status
- overall implementation status
- phase-by-phase verification
- evidence
- confidence level
- divergences between PRD, plan, and code
- unresolved decisions or unclear areas
- the recommended next step
- recommended doc updates, if any

The report should make it easy for another agent to continue work, but the plan remains the main execution document.
Keep one current resume file per slug; refresh it when stale rather than building up local resume history by default.

## References

- Use [references/resume-checklist.md](references/resume-checklist.md) for what evidence to inspect.
- Use [references/resume-output-template.md](references/resume-output-template.md) for the report format.
- Use `.wilco/index/<slug>.json` as the preferred machine-readable linkage file when present.
- Use [../wilco-docs/references/status-vocabulary.md](../wilco-docs/references/status-vocabulary.md) for shared status terms.

If the reconciliation shows the document lifecycle itself is unclear, also use `wilco-docs`.
