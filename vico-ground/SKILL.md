---
name: vico-ground
description: Build just enough shared ground to choose a safe next route before planning or execution. Use when the user wants to orient in a repo, inspect a design, clarify intent or scope, pressure-test a proposal, or hand current understanding forward into vico-plan.
---

# Vico Ground

`vico-ground` is the lightweight grounding controller in Vico.

Build just enough shared ground to choose a safe next route.
Do not keep grounding once the next safe route is already clear.

Treat natural requests such as `scan the repo`, `inspect the codebase`, `take a quick pass over the project`, `orient me in this repo`, `clarify this`, `what are we actually solving`, `align on terms`, `stress-test this`, `challenge this assumption`, `review what we know`, `resolve this into a handoff`, or `how do I use vico-ground` as valid entrypoints even when the user does not name the skill explicitly.

Treat short repo-orientation requests as strong `vico-ground` signals by default, especially when the user is asking for overall structure, architecture, boundaries, assumptions, or a fast repo scan.

Do not force `vico-ground` for every short inspection request. If the wording clearly asks for a narrow direct answer, a one-off file read, or immediate implementation, route normally. When the same phrase could mean either quick inspection or explicit shared-ground building, prefer one short clarification rather than silently skipping the skill.

## Agent Summary

- `Display name`: `Vico Ground`
- `Short description`: `Build shared ground before planning or execution`
- `Default prompt`: `Build just enough shared ground to choose a safe next route. Keep the public interface small: prefer `scan`, `clarify`, `stress`, or `handoff`; stop grounding once the next route is clear; ask rather than guess when uncertainty is material; and emit a thin ground handoff when the next consumer is vico-plan. Think before acting: prefer the minimum grounding move that resolves the highest-value uncertainty.`

## Public Moves

`vico-ground` keeps a small public interface:

- `scan`
  - build enough factual confidence to choose the next route
- `clarify`
  - align on goals, scope, terms, or constraints
- `stress`
  - pressure-test a proposal, assumption, or plan
- `handoff`
  - stop grounding and emit the next route clearly
- `help`
  - show the compact interface and common entrypoints

The following are internal submodes rather than primary public moves:

- `align`
  - handled inside `clarify`
- `reframe`
  - handled as a `clarify` or `scan` outcome when the current frame is wrong
- `tradeoff`
  - handled inside `stress`
- `grill`
  - handled inside `stress`
- `challenge`
  - handled inside `stress`
- `review`
  - handled inside `handoff`
- `resolve`
  - handled inside `handoff`
- `map`
  - optional artifact that `scan` may produce when structure matters

## Controller Rules

Choose the smallest move that resolves the highest-value uncertainty.

Prefer:

- `scan` when facts are weak
- `clarify` when objective, scope, terms, or constraints are weak
- `stress` when a proposal, assumption, plan, or option set needs pressure
- `handoff` when the next safe route is already clear

When multiple moves are plausible, prefer the one that most reduces harmful uncertainty while keeping the public surface small.

## Stop Rule

Stop grounding as soon as one of these becomes true:

- the next safe route is clear
- the next blocking question belongs to planning or execution rather than grounding
- further grounding would mostly repeat or reformat conclusions that already exist

Never continue grounding just to make the output look more complete.

## Minimal State Model

Use only the smallest state needed to act safely:

- `Facts`
  - evidence-backed conclusions safe enough to lean on
- `Assumptions`
  - temporary working beliefs that still carry uncertainty
- `Tensions`
  - unresolved tradeoffs, disagreements, or open choices
- `Next route`
  - where the work should go next

Do not force a larger state model into user-facing output unless the user explicitly wants that detail.

## Output Contract

Every move-driven output should begin with exactly one visible line: `Move: <move>`.

If route-debug context is needed, prefer surfacing it in a short update immediately before the move-driven output rather than inserting lines ahead of `Move: <move>`.

Default output should stay compact and include:

- `Conclusion`
- `Evidence`
- `Next route`
- `Recommended next action`

Optional sections:

- `Other next actions`
- `Assumptions`
- `Tensions`
- `Why this matters`

Keep machine-facing literals stable.
Use the user's primary working language when it is clear from the conversation.
When route selection may be non-obvious, surface this route-debug shape in the first visible update when `vico-ground` is selected:

- `Skill route: vico-ground`
- `Route reason: <explicit_skill_request | intent_cluster | natural_trigger>`
- optional `Route detail: <repo_orientation | architecture_scan | exact trigger phrase>`
- optional `Route mode: <scan | clarify | stress | handoff>`

## Move Contracts

### `scan`

Use `scan` to build enough factual confidence to choose the next route, not to fully model the target.

Minimum output:

- `Conclusion`
- `Evidence`
- `Next route`
- `Recommended next action`

`scan` may include a structural map when the shape of the system is itself the blocker, but that map is optional.
When more than one safe follow-up exists, keep one clearly preferred action under `Recommended next action` and put 1-3 concise alternatives under `Other next actions`.

### `clarify`

Use `clarify` when the main gap is about goals, scope, terms, constraints, or framing.

- repair terminology or boundary mismatches here instead of exposing a separate `align` route
- if the current interpretation is wrong, replace it here instead of exposing a separate `reframe` route

### `stress`

Use `stress` when the current proposal, assumption, plan, or option set needs pressure.

`stress` can internally take one of these shapes:

- `check`
  - quick weakness scan
- `tradeoff`
  - compare live options and costs
- `challenge`
  - apply stronger counterexamples or rebuttals

Keep `stress` focused on pressure that changes the next route or decision.

### `handoff`

Use `handoff` when grounding should stop and the next route should be made explicit.

`handoff` replaces the old public split between `review` and `resolve`.

- use a brief handoff when the user mainly needs a checkpoint and next route
- use a full handoff only when another workflow, especially `vico-plan`, needs structured transfer

## Full Handoff Contract

Only emit a full `## Ground Handoff` block when another workflow needs structured transfer.

Required fields:

- `Target`
- `What is true now`
- `What is still unresolved`
- `Recommended route`
- `Suggested first step`

Optional fields:

- `Suggested slug`
- `Tracking hint`
  - `no-doc`
  - `plan_only`
  - `prd_backed`

Keep the handoff thin. `vico-plan` should plan from this handoff, not depend on a bloated pre-plan schema.

## References

- Use [references/index.md](references/index.md) as the quick entrypoint into `references/`.
- Use [references/help-template.md](references/help-template.md) for `vico-ground help`.
- Use [references/move-selection-cheatsheet.md](references/move-selection-cheatsheet.md) as a quick routing aid.
- Use [references/scan-template.md](references/scan-template.md) for the compact `scan` shape.
- Use [references/handoff-template.md](references/handoff-template.md) for full `vico-plan` handoff shape.
- Use [references/stress-modes.md](references/stress-modes.md) for internal `stress` submodes.
- Use [references/output-format.md](references/output-format.md) for worked examples and anti-examples.
- Use [references/anti-patterns.md](references/anti-patterns.md) as a quick failure-mode checklist.
