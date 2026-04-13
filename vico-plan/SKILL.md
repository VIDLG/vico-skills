---
name: vico-plan
description: Default front door for Vico-style repo-local planning. Decide whether work should stay `no-doc`, become `plan_only`, or upgrade to `prd_backed`; reconcile active state when needed; then create or update the active plan under `.vico/plans/active/`. Use when the user wants to start tracked work, make a plan, create a tracked plan, continue tracked work, recover from Vico drift, or turn grounded decisions into an executable plan.
---

# Vico Plan

## Overview

`vico-plan` is the default front door for tracked Vico work.

Treat natural requests such as `make a plan`, `create a tracked plan`, `turn this into execution steps`, `reconcile the current plan`, `verify this plan`, or `how do I use vico-plan` as valid `vico-plan` entrypoints even when the user does not name the skill explicitly.

Treat tracked-work controller intent as the main routing signal. Use `vico-plan` by default when the user is trying to start tracked work, reshape the execution contract, verify tracked completion, or continue an existing tracked thread without asking for persistent implementation looping yet.

If the user's intent could reasonably map to lightweight direct execution instead of tracked planning, and repository evidence does not clearly justify `.vico` tracking, ask a short clarification question before creating tracked work.
If the user's wording mainly signals persistent implementation continuation and an active plan already exists, prefer `vico-exec` instead of `vico-plan`.

## Agent Summary

- `Display name`: `Vico Plan`
- `Short description`: `Default to plan_only and write Vico execution plans`
- `Default prompt`: `Act as the default front door for Vico planning. Decide whether work should stay `no-doc`, become `plan_only`, or upgrade to `prd_backed`; perform lightweight reconcile when active state is stale or overlapping; choose the clearest active execution contract; absorb the latest `vico-ground` handoff block by default; and then update the active plan under .vico/plans/active with derived index alignment as needed. Apply simplicity first: prefer the smallest execution contract that can guide reliable work, ask rather than guess when tracking scope is materially ambiguous, and avoid speculative phases or abstractions.`

It owns four decisions before planning:

1. should this stay `no-doc`
2. should this be `plan_only`
3. should this upgrade to `prd_backed`
4. does the current active slug need reuse, repair, or replacement

After that, it writes or updates the active plan under `.vico/plans/active/`.
Default to a single active plan document that carries both intent and execution. When work outgrows that shape, upgrade the slug to `prd_backed` and keep the plan as the execution document. Prefer dated slugs, capture status and dates in metadata, and prefer vertical slices over horizontal layer-by-layer plans.
Route repo-local lifecycle and maintenance operations through `vico-ops`.

## Simplicity Discipline

- Build the minimum execution contract that solves the current planning problem.
- Do not add speculative phases, abstractions, or artifacts just because they might be useful later.
- If `plan_only` is sufficient, do not escalate to `prd_backed`.
- If a smaller plan shape can support reliable execution, prefer it.
- Keep every planned slice directly tied to the user's requested outcome.

## Forward-Only Planning Discipline

- Default to forward design and assume no historical burden unless the user explicitly says compatibility matters.
- Prefer clean replacement over compatibility scaffolding when the old execution contract is now confusing.
- Do not preserve legacy names, aliases, plan shapes, or stale workflow branches by default.
- Prefer one clear active execution contract over overlapping transitional artifacts.

The plan is the primary execution document. Its checklist defines the intended path of work and the smallest next executable units.

Default to `plan_only` when that is sufficient. A PRD is an escalation, not a baseline requirement.
When a slug is `prd_backed`, this skill owns the plan side of that contract and keeps its execution details current.
When the current state is unclear, this skill performs the minimum reconcile needed before rewriting the plan.
When a recent `vico-ground` handoff block exists in the current conversation, this skill should consume that ground handoff by default.
When work re-enters tracked planning after direct execution, perform the minimum reconcile or sync needed to align active docs with current repository reality before planning further.
Treat that re-entry behavior as first-class rather than exceptional; do not assume the user stayed inside tracked workflow the whole time.

## Input Sources

`vico-plan` may receive input from:

- direct user intent in the current turn
- the current active plan and optional active PRD
- current code and test state
- the latest `vico-ground` handoff block in the current conversation

Treat these as ordered inputs, not as peer truth sources.
Treat them as one planning input bundle after precedence has been resolved; do not let the last conversational subtopic silently replace the broader work object.

## Input Precedence

When multiple inputs are present, resolve them in this order:

1. explicit user input
2. matching `vico-ground` handoff
3. current active plan / optional active PRD
4. current code reality

Use code reality to verify and correct stale planning state, but do not let it silently override explicit user intent or a matching current-turn handoff.

Treat a ground handoff as matching only when:

- its optional `Suggested slug` matches the tracked work in scope, or
- when no slug exists yet, its `Target` clearly matches the current requested work object

Treat `Tracking hint` in the handoff as a soft routing hint:

- `no-doc` may justify staying light
- `plan_only` is the default tracked mode
- `prd_backed` may justify creating or updating a paired PRD

If the latest ground handoff clearly targets a different active slug or work object than the current request, do not absorb it implicitly.
If a matching ground handoff came from a broad scan or architectural pass, treat it as describing the whole tracked work object rather than just the last grounded issue.

## Mode Contract

`vico-plan` should support these explicit modes:

- default
  - create, update, or reconcile tracked work
- `help`
  - show the controller modes, input sources, and common examples
- `review`
  - inspect the current active state and report it without writing any docs
- `verify`
  - check the active plan against current code and test evidence before close-out, without writing any docs
- `prd`
  - upgrade or update `prd_backed` state
- `replan`
  - rewrite the current execution contract under the same slug

`review` must be strictly read-only.
`verify` must be strictly read-only.
Use `replan` as the single public mode for same-slug execution-contract rewrites. Do not expose a separate public `reset` mode.
Route lifecycle and maintenance follow-ups such as `close`, `cancel`, `truth`, `sync`, or workspace validation through `vico-ops` rather than exposing them as `vico-plan` public modes.

## Workflow

1. Determine whether the work should stay `no-doc` or enter tracked planning.
2. Inspect active `.vico` state and decide whether the request:
   - reuses one active slug
   - upgrades one active slug from `plan_only` to `prd_backed`
   - replaces an active slug with one fresh dated slug
   - or needs one new dated slug
3. Reconcile current implementation reality if active state is stale, unclear, or overlapping.
4. If the work should stay `no-doc`, stop. Do not create a plan.
5. Determine the tracking mode:
   - `plan_only` by default
   - `prd_backed` only when the work clearly needs a separate PRD
6. If `prd_backed`, ensure the paired PRD exists and its header points back to the plan.
7. If a recent `vico-ground` handoff block exists, absorb these as strong inputs:
   - `Target`
   - `What is true now`
   - `What is still unresolved`
   - `Suggested first step`
   And absorb these as soft execution-shaping hints when present:
   - optional `Suggested slug`
   - optional `Tracking hint`
8. Explore the codebase to understand current architecture, ownership, and integration seams.
9. Identify durable architectural decisions that should apply across all phases.
10. Draft thin vertical slices that produce verifiable behavior end-to-end.
11. If slice granularity or scope remains materially ambiguous, review it with the user and iterate until safe.
12. Update `.vico/index/<slug>.json` as a derived machine-readable link to the primary artifacts. Prefer [scripts/sync_vico_index.py](scripts/sync_vico_index.py) when available instead of hand-editing derived linkage.
13. Write or update the plan at `.vico/plans/active/<slug>.md` using [references/templates/plan-template.md](references/templates/plan-template.md). Prefer [scripts/sync_vico_headers.py](scripts/sync_vico_headers.py) when header cross-links drift.
14. If there is a source PRD, update the PRD header so `Execution Plan` points to the new plan path.
15. If overlap handling is more complex than a clean rewrite, prefer a fresh dated slug over preserving a confusing lineage.
16. When repo-local maintenance is now the real need, hand off to `vico-ops` instead of expanding the planning surface.

## Multi-Active Safety Rules

- `review` may summarize all active slugs, but should identify which one appears most relevant and why.
- `replan` and `prd` should prefer explicit slug selection when multiple active slugs are materially plausible.

## Planning Rules

- Use one dated slug across the active plan and any optional active PRD for the same execution contract.
- Prefer one fresh dated slug over complicated overlap handling when the existing active slug is no longer the clearest execution contract.
- Keep implementation plans repo-local; do not default to `./plans/`.
- Use tracer-bullet vertical slices, not horizontal batches of layer-specific work.
- Keep the tracked scope anchored to the full accepted work object; do not let one clarified issue collapse a broader refactor or cleanup program unless the user explicitly narrows scope.
- Acceptance criteria should describe observable outcomes, not implementation chores.
- Put status and dates in the header so age and freshness remain obvious to humans and agents.
- Mark the plan mode explicitly:
  - `Mode: plan_only` when the plan is the only active tracked document
  - `Mode: prd_backed` when the slug also has an active PRD
- Do not force a PRD for every task. Small, clear, implementation-facing work should remain `plan_only`.
- Do not create a new plan when the work clearly advances an existing active slug.
- If work hits an existing active slug, do not treat it as `no-doc`; update the plan even for small implementation-facing advances.
- Keep the checklist. The checklist is the execution anchor that `vico-exec` should work from; temporary reconcile only validates it when needed.
- Treat reconcile as an internal planning capability, not as a separate default user-facing step.
- Treat PRD creation as an internal escalation path, not as a separate default user-facing step.
- Treat new-slug bootstrap as an internal planning capability, not as a separate default user-facing step.
- Prefer checklist items that are small, behavior-oriented, and verifiable.
- A broad scan plus grill sequence should usually produce one coordinated plan with multiple slices, not a single-issue plan, unless the user explicitly requests a narrower contract.
- If tracked work advances, even via a tiny "vibe" change, sync the plan checklist and `Updated` date instead of silently relying on code state.
- If scope, goals, or acceptance moved enough that the plan is no longer the right execution contract, upgrade or update the paired PRD inside this workflow.
- If a request introduces a clearly new or cleaner execution contract, start a new dated slug instead of stretching the old one.
- If overlap handling becomes awkward, prefer a fresh dated slug and route any destructive cleanup through `vico-ops`.
- If a `plan_only` slug is upgraded to `prd_backed`, update plan header metadata, PRD header metadata, and index linkage atomically.
- Do not support in-place downgrade from `prd_backed` to `plan_only`.
- Treat the plan as the main human-readable execution artifact. The index is supporting metadata, not peer-level prose.

## Execution Readiness Rules

- A plan is `vico-exec` ready only when the next smallest unblocked slice can be chosen without guessing beyond the current plan or PRD.
- The current slice should expose observable acceptance criteria and at least one focused verification path.
- User decisions, blockers, and unresolved scope forks should be explicit in the plan or PRD rather than implied by missing checklist detail.
- If the current plan is too coarse, too stale, or too ambiguous for the next step to be chosen reliably, stay in `vico-plan` and reconcile or `replan` before routing into `vico-exec`.
- Prefer using ground handoff hints to sharpen the first execution slice when they materially reduce ambiguity.
- Treat `What is true now` as grounded context that should sharpen planning unless repository evidence now conflicts with it.

## Verification Rules

- `verify` is the close-out readiness gate for tracked work.
- `verify` must compare the active plan and optional PRD against current code and test evidence instead of trusting `.vico` status alone.
- Use `verify` when another agent claims the work is complete, when `Status` or checklist state may be stale, or before `vico-ops close` deletes active docs.
- `verify` should produce a completion verdict:
  - `verified_complete`
  - `not_complete`
  - `ambiguous`
- `verify` alone must not delete active docs or silently close out the slug.
- If the verdict is not `verified_complete`, prefer `replan`, `prd`, or resumed execution over lifecycle cleanup.
- In multi-active situations, `verify` should require an explicit slug unless the target is unambiguous from current-turn user steering.
- If completion evidence is strong, stop after `verify` and recommend `vico-ops close` instead of deleting active docs.

## Sync Contract

- `no-doc` with no slug hit: do not create a plan
- new tracked work with no slug hit: create one fresh dated slug here
- existing slug, implementation advance only: update the plan and minimally refresh the index
- existing slug, plan no longer matches implementation: perform `diverge-replan`
- existing slug, plan no longer sufficient for scope framing: perform `upgrade-to-prd-backed` here
- existing slug, task completed: keep the active docs and route lifecycle cleanup through `vico-ops`

## Output Contract

Write plans with at least:

- `Status`
- `Mode`
- optional `Progress`
- `Created`
- `Updated`
- optional `Manifest`
- optional `Source PRD`
- optional `What is still unresolved`
- architectural decisions section
- phased slices
- acceptance criteria per phase

For user-facing textual output:

- use the user's primary working language when it is clear from the conversation
- if the user's preferred language is unclear, mirror the user's most recent substantive message
- keep commands, mode names, file paths, code literals, and machine-consumed handoff field names stable unless that downstream contract is explicitly changed
- keep internal routing and reconciliation heuristics implicit by default unless they materially affect the user's next planning decision
- surface this route-debug shape in the first visible update when `vico-plan` is selected:
  - `Skill route: vico-plan`
  - `Route reason: <explicit_skill_request | intent_cluster | natural_trigger>`
  - optional `Route detail: <tracked_work_controller | verify_request | exact trigger phrase>`
  - optional `Route mode: <review | verify | prd | replan>`

For `help`:

- list modes
- list input precedence
- show 2-4 concrete examples

For `review`:

- show active slug(s)
- show tracking mode
- show current phase / progress
- show likely drift risk
- do not write any docs

For `verify`:

- show the selected slug
- show the completion verdict
- show evidence from current code and tests
- show open gaps between plan state and repository reality
- show `Recommended action` using one of:
  - `direct_execute`
  - `vico-plan`
  - `vico-plan -> vico-exec`
- show the recommended next mode
- do not write any docs

Use the full phased template for medium and large work. For small plan-only work, use the lighter plan-only template.

## References

- Use [references/templates/plan-template.md](references/templates/plan-template.md) for the repository plan template.
- Use [references/templates/plan-only-template.md](references/templates/plan-only-template.md) for smaller plan-only work.
- Use [references/templates/prd-template.md](references/templates/prd-template.md) for the internal `prd_backed` upgrade path.
- Use [references/templates/help-template.md](references/templates/help-template.md) for `vico-plan help`.
- Use [references/templates/review-template.md](references/templates/review-template.md) for `vico-plan review`.
- Use [references/templates/verify-template.md](references/templates/verify-template.md) for `vico-plan verify`.
- Use [references/templates/ground-handoff-template.md](references/templates/ground-handoff-template.md) for the expected `vico-ground` handoff block shape.
- Use [references/ops/reconcile.md](references/ops/reconcile.md) when reconcile is needed before planning.
- Use [references/rules/status-vocabulary.md](references/rules/status-vocabulary.md) when expressing progress or divergence.
- Use [references/ops/automation.md](references/ops/automation.md) for repo-local planning automation context and `vico-ops` handoff boundaries.
- Use [references/rules/routing.md](references/rules/routing.md) when deciding reuse / replace / PRD escalation or when active state is messy.
- Use [references/rules/layout.md](references/rules/layout.md) when updating long-lived truth in `docs/architecture/`.
- Use [scripts/bootstrap_vico_slug.py](scripts/bootstrap_vico_slug.py) when this workflow decides a new tracked slug is needed.
- Use `.vico/index/<slug>.json` as the machine-readable linkage file for cross-agent coordination.
