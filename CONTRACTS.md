# Wilco Contracts

This document is the governance map for ownership, derivation, and validation boundaries.
It is not the user-facing workflow guide and not a second source of skill behavior truth.

## Distribution Assumptions

- Runtime should be safe for single-skill installation and use.
- Runtime must not depend on the repository-root `README.md`.
- Runtime must not depend on cross-skill paths.
- Shared runtime needs must be satisfied through owner sources plus skill-local closures.

## Persistence Policy

- `wilco-probe` state is session-local by default and should not be written back unless the user explicitly asks.
- `wilco-plan` owns tracked-doc writes for active plan, optional PRD, and derived index state.
- `wilco-exec` may write plan, index, or temporary reconcile state when execution continuity depends on accurate persisted state.

## User-Facing Vs Internal

- User-facing output should prioritize the smallest set of conclusions, decisions, and next steps needed for productive continuation.
- Internal state may remain richer than user-facing output when that extra detail mainly serves routing, continuity, or validation.
- Do not dump the full internal scheduler, issue bank, or execution heuristics into default user-facing output unless the user asks for that detail or it materially affects the next decision.
- Keep machine-consumed fields stable even when surrounding prose is optimized for user readability.
- When a Wilco skill is selected, expose the active skill route and route reason in the first visible update so the user can distinguish skill-routed behavior from generic model behavior.
- When a human-facing checkpoint, summary, verification result, or handoff is emitted, prefer a `Recommended action` when that action is not already obvious.
- Standardize `Recommended action` on:
  - `direct_execute`
  - `wilco-plan`
  - `wilco-plan -> wilco-exec`

## Verification Authority

- `Status`, checklist completion, and index linkage are operational planning signals, not final proof of completion.
- Final close-out decisions should be gated by current repository evidence via `wilco-plan verify`.

## Public Modes Vs Status Values

- Public workflow actions should use stable mode names such as `close`, `cancel`, `verify`, `sync`, and `replan`.
- Status and progress literals such as `done`, `partial`, and `not_started` remain state vocabulary rather than public close-out command names.

## External Side Effects

- External side effects such as creating, reopening, commenting on, or closing GitHub issues require explicit user confirmation by default.
- Draft generation and duplicate checking are safe defaults; mutating external systems is not.

## Contract Layers

1. `Global workflow constitution`
   Owner source: [README.md](README.md)
2. `Skill behavior contracts`
   Owner source: each `<skill>/SKILL.md`
3. `Shared structural contracts`
   Owner sources: the owning template, reference, or shared-script source file

## Owners And Derived Forms

| Contract type | Owner source | Derived forms | Validator responsibility |
| --- | --- | --- | --- |
| Global workflow constitution | `README.md` | skill-level references, contract map entries, workflow invariant checks | ensure README markers exist and downstream docs do not drift on core invariants |
| Skill behavior contract | each `<skill>/SKILL.md` | `<skill>/agents/openai.yaml`, skill-local references, examples | ensure the skill body is present, referenced helpers exist, and agent summaries do not become a second full contract |
| Shared scripts | owner script file, currently under `wilco-plan/scripts/` | skill-local wrapper entries under `<skill>/scripts/` when still needed | ensure owner source exists, local wrapper entry points exist where required, and runtime references do not point across skill boundaries |
| Shared status and decision rules | owner reference file, currently under `wilco-plan/references/` | skill-local full reference copies where runtime visibility is required | ensure owner files exist, local copies exist where required, and copies are treated as derived content |
| Strong templates | owner template file, such as `plan-template.md`, `prd-template.md`, `reconcile-output-template.md` | skill-local visible copies or references needed for runtime closure | ensure owner templates exist, required local closures exist, and key structure remains stable |
| Feedback / issue templates | owner template file under `wilco-feedback/references/` | issue drafts and filing behavior in `wilco-feedback` | ensure draft templates exist, stay concise, and keep confirmation boundaries explicit |
| Contract map | `CONTRACTS.md` and `CONTRACTS-zh.md` | README links | ensure the map exists and keeps owner/derived/validation responsibilities aligned |

## Sync Policy

- Owner sources are edited directly.
- Derived forms are synchronized from owner sources.
- Derived forms are read-only by default.
- If a derived file needs owner-specific additions, the derived block and the owner-local block must be explicitly separated.
- Do not create a new top-level shared source directory just to deduplicate content.
- Only synchronize high-repeat, structurally stable, cross-skill content.

### First Migration Order

1. shared scripts
2. status and decision rules
3. strong structural templates

## Validation Responsibilities

Validator checks should be explicit rather than generic. At minimum they should cover:

- owner source existence
- derived-form presence
- sync-boundary enforcement
- read-only generated content rules

## Notes

- This document maps governance boundaries. It does not replace README, SKILL.md, or owner templates.
- When a contract changes, update the owner source first, then refresh derived forms, then update validator coverage.
