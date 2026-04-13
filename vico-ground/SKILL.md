---
name: vico-ground
description: Build shared ground between the user, the repository, and the current work object before planning or execution. Use when the user wants to clarify intent, inspect a repo or design, scan or orient around a codebase, map assumptions, align terminology, reframe the problem, surface tradeoffs, pressure-test a proposal, review current understanding, export the current operating brief, or resolve the current ground into a handoff for vico-plan.
---

# Vico Ground

`vico-ground` is the shared-ground construction workflow in Vico.

Treat natural requests such as `scan the repo`, `inspect the codebase`, `scan the architecture`, `take a quick pass over the project`, `orient me in this repo`, `clarify this`, `what are we actually solving`, `align on terms`, `map the decision`, `map the problem`, `reframe this`, `surface the tradeoff`, `stress-test this`, `grill this plan`, `challenge this assumption`, `review what we know`, `where are we disagreeing`, `export these rules to AGENTS.md`, `write the operating brief to CLAUDE.md`, `resolve this into a handoff`, or `how do I use vico-ground` as valid entrypoints even when the user does not name the skill explicitly.

Treat short repo-orientation requests as strong `vico-ground` signals by default, especially when the user is asking for overall structure, architecture, boundaries, assumptions, or a fast repo scan.

Do not force `vico-ground` for every short inspection request. If the wording clearly asks for a narrow direct answer, a one-off file read, or immediate implementation, route normally. When the same phrase could mean either quick inspection or explicit shared-ground building, prefer one short clarification rather than silently skipping the skill.

## Theory Basis

`vico-ground` is designed around:

- common ground
- conversational grounding
- sensemaking
- collaborative problem solving
- deliberation and argumentation
- preference reconciliation

The goal is not merely to answer. The goal is to build enough shared ground for safe action.

## Grounding Principles

- Do not assume missing intent when a short clarification question would remove real ambiguity.
- Do not hide confusion behind overconfident prose. Name the exact uncertainty.
- Surface tradeoffs explicitly when multiple live options still exist.
- If uncertain, ask rather than guess.
- Do not pick silently when ambiguity exists.
- Build and maintain shared ground, not just local model confidence.

## State Model

`vico-ground` should organize session-local state around:

- `Objective`
  - the higher-level outcome the user is trying to reach
- `Target`
  - the current object being grounded: repo, plan, PRD, design, proposal, or decision
- `Accepted Facts`
  - facts grounded strongly enough to act on
- `Active Assumptions`
  - temporary assumptions still carrying uncertainty
- `Interpretations`
  - current explanatory frames placed on top of the facts
- `Findings`
  - user-facing diagnostic conclusions
- `Preferences`
  - value orderings, priorities, and non-factual constraints expressed by the user or team
- `Issue Bank`
  - the internal set of real problems, conflicts, gaps, or unresolved decisions worth triaging
- `Tradeoffs`
  - active tensions among options, constraints, costs, and reversibility
- `Commitments`
  - rules, decisions, or operating constraints the next workflow should treat as binding unless re-opened explicitly
- `Open Questions`
  - unresolved points that still block strong grounding
- `Topic Map`
  - the current structural map of the shared problem space
- `Ground Handoff`
  - the summary that the next workflow should consume

Do not treat every `Finding` as an `Issue`.
Findings may include issue-backed risks, stable observations, or structure notes that improve the user's mental model.
Only promote a finding into the `Issue Bank` when it represents a real problem, conflict, gap, or unresolved decision worth triaging.

## Epistemic Status Model

Every meaningful grounding artifact should be understood as one of these:

- `fact`
  - strongly grounded by evidence and safe to act on
- `assumption`
  - temporarily accepted but still uncertain
- `interpretation`
  - a current explanation layered on top of facts
- `preference`
  - a value choice, priority, or non-factual constraint
- `commitment`
  - a decision or rule that downstream workflows should now treat as active

Do not silently upgrade an assumption into a fact.
Do not silently present a preference as if it were a discovered fact.
Do not silently present an interpretation as if it were the only possible frame.

## Epistemic Transition Rules

Use these as the default transition rules for grounding state:

- `assumption -> fact`
  only when new evidence grounds it strongly enough to act on
- `interpretation -> replaced`
  when `reframe` produces a better explanation and the old frame is no longer primary
- `finding -> issue`
  only when the finding represents a real problem, conflict, gap, or unresolved decision worth triaging
- `preference -> commitment`
  only when the user or team clearly accepts that preference as an active downstream rule
- `fact -> questioned`
  only when new evidence materially weakens it; do not reopen grounded facts casually

When a transition happens:

- name the old status
- name the new status
- cite the evidence or user signal that justified the transition

## Moves

`vico-ground` should support these explicit moves:

- default
  - act as a controller and choose the highest-value next grounding move
- `clarify`
  - align goals, scope, terms, and success criteria
- `scan`
  - inspect the target and build evidence, findings, issues, and a topic map
- `map`
  - externalize the structure of the problem, dependencies, or decision space
- `align`
  - repair vocabulary, boundary, or assumption mismatches
- `reframe`
  - replace the current interpretation or problem frame when the current frame is too narrow or misleading
- `tradeoff`
  - reconcile preferences, constraints, risks, and irreversibilities
- `grill`
  - pressure-test assumptions, findings, plans, maps, or proposed decisions
- `challenge`
  - use adversarial review, counterexamples, and rebuttals to test the current ground
- `review`
  - checkpoint the current shared ground without expanding it
- `export-md`
  - export the current shared ground and operating discipline into `AGENTS.md` or `CLAUDE.md`
- `resolve`
  - compress the current shared ground into a decision, recommendation, or handoff
- `help`
  - show the moves and common usage patterns

## Controller Rules

When no explicit move is given, choose the next move by asking:

`what is the highest-value missing condition for actionable shared ground?`

Prefer:

- `clarify` when objective, scope, or success criteria are ambiguous
- `scan` when factual grounding is weak
- `map` when structure is still fuzzy
- `align` when terms or boundaries are inconsistent
- `reframe` when the current interpretation is too narrow, stale, or misleading
- `tradeoff` when the real gap is priority or preference reconciliation
- `grill` when the current proposal needs adversarial pressure
- `challenge` when the current ground needs counterexamples, adversarial review, or rebuttal
- `review` when the user needs a checkpoint
- `export-md` when the current shared ground should become a durable repo-local operating brief
- `resolve` when the current ground is sufficient for the next workflow

## Move Selection Rubric

When multiple moves are plausible, rank them using these questions:

- is the highest-value missing condition about intent or scope
  - prefer `clarify`
- is the highest-value missing condition about factual reality
  - prefer `scan`
- is the highest-value missing condition about structural understanding
  - prefer `map`
- is the highest-value missing condition about vocabulary or boundary mismatch
  - prefer `align`
- is the highest-value missing condition that the current frame itself is wrong
  - prefer `reframe`
- is the highest-value missing condition about preference, priority, or irreversibility
  - prefer `tradeoff`
- is the highest-value missing condition about robustness under pressure
  - prefer `grill`
- is the highest-value missing condition about rebuttal, counterexample, or adversarial review
  - prefer `challenge`
- is the user mainly asking for a checkpoint
  - prefer `review`
- is the current ground already actionable and ready to hand forward
  - prefer `resolve`
- should the current ground now become durable repo-local instructions
  - prefer `export-md`

Then break ties using these dimensions:

- `ambiguity_reduction`
  how much this move reduces the most harmful uncertainty
- `dependency_unlock`
  how many downstream moves become cleaner after this move
- `irreversibility`
  how costly it is to defer this move
- `coordination_risk`
  how much team or agent confusion persists if this move is skipped
- `verification_impact`
  how much this move improves the quality of later verification

## Scan Contract

`scan` should build an evidence-first picture of the target.

- establish evidence before committed questioning
- produce user-facing `Findings`
- maintain the fuller internal `Issue Bank`
- keep `Findings` and `Issues` distinct
- avoid unstructured summary drift

Use this default shape:

- `<target> | <topic-path>`
- `Mode: concise | available: concise, detailed`
- optional `Priority: critical|important|detail`
- optional `Intent overlay`
- `Findings`
- `Evidence`
- `Topic map snapshot`
- `High-risk gaps`
- `Likely recommendations`
- `Open questions worth asking`
- `Suggested next move`

## Grill Contract

Use `grill` when the next best action is adversarial clarification or pressure-testing rather than more evidence gathering.

- `grill` may target assumptions, findings, tradeoffs, plans, maps, or proposed decisions
- prefer one active question at a time
- use counterexamples, edge cases, and irreversibility checks when useful
- allow direct recommendation when one option clearly dominates and another question would be performative
- support short answer modifiers:
  - `rec`
  - `do`
  - `hold`
  - `cont`
  - `close`

## Challenge Contract

Use `challenge` when the current ground needs adversarial review rather than ordinary clarification.

- test the current claim set against counterexamples
- surface rebuttals and hidden failure modes
- distinguish factual disagreement from preference disagreement
- keep the challenge attached to the current shared ground rather than restarting the workflow from zero

## Reframe Contract

Use `reframe` when the current interpretation is itself the problem.

- identify the current frame explicitly
- state why it is too narrow, stale, or misleading
- propose a better framing
- preserve any still-valid accepted facts while replacing the old interpretation

## Export Contract

Use `export-md` when the current shared ground should become a durable repo-local operating brief.

- export the current operating discipline into `AGENTS.md` or `CLAUDE.md`
- include clarification, simplicity, surgical edit, and success criteria discipline
- include active context when a single active slug is clearly in scope
- do not overwrite an existing file unless the user explicitly asks

## Resolve Contract

Use `resolve` when the current shared ground is sufficient to hand the work forward.

- summarize accepted facts
- summarize accepted decisions
- name active assumptions
- name remaining open questions
- include key tradeoffs when they affect downstream execution
- emit a self-contained `## Ground Handoff` block when the next clear consumer is `vico-plan`

## Output Contract

For user-facing output:

- use the user's primary working language when it is clear from the conversation
- if language is unclear, mirror the most recent substantive message
- keep commands, mode names, file paths, and machine-consumed field names stable

Preferred top-level sections:

- `Accepted facts`
- `Accepted decisions`
- `Active assumptions`
- `Interpretations`
- `Preferences`
- `Tradeoffs`
- `Commitments`
- `Open questions`
- `Recommended next action`

## References

- Use [references/help-template.md](references/help-template.md) for `vico-ground help`.
- Use [references/output-format.md](references/output-format.md) for output examples.
- Use [scripts/export_vico_operating_md.py](scripts/export_vico_operating_md.py) for `vico-ground export-md`.
