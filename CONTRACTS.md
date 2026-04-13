# Vico Contracts

This document is the governance map for ownership, derivation, and validation boundaries.
It is not the user-facing workflow guide and not a second source of skill behavior truth.

## Distribution Assumptions

- Runtime should be safe for single-skill installation and use.
- Runtime must not depend on the repository-root `README.md`.
- Runtime must not depend on cross-skill paths.
- Shared runtime needs must be satisfied through owner sources plus skill-local closures.

## Persistence Policy

- `vico-ground` state is session-local by default and should not write `.vico` artifacts unless the user explicitly asks to capture or export conclusions.
- `vico-plan` owns tracked-doc writes for active plan, optional PRD, and derived index state.
- `vico-exec` may write plan, index, or temporary reconcile state when execution continuity depends on accurate persisted state.

## User-Facing Vs Internal

- User-facing output should prioritize the smallest set of conclusions, decisions, and next steps needed for productive continuation.
- Internal state may remain richer than user-facing output when that extra detail mainly serves routing, continuity, or validation.
- Do not dump the full internal scheduler, issue bank, or execution heuristics into default user-facing output unless the user asks for that detail or it materially affects the next decision.
- Do not present ungrounded or assumption-level `vico-ground` conclusions as if they were repository-backed findings or tracked-plan commitments.
- Keep machine-consumed fields stable even when surrounding prose is optimized for user readability.
- When a Vico skill is selected, expose the active skill route and route reason in the first visible update so the user can distinguish skill-routed behavior from generic model behavior.
- Prefer this minimal route-debug shape:
  - `Skill route: <skill-name>`
  - `Route reason: <explicit_skill_request | intent_cluster | natural_trigger>`
  - optional `Route detail: <the strongest route-specific detail>`
  - optional `Route mode: <public mode or move>` when a specific mode already explains the route more clearly
- For explicit invocations, say that the route came from an explicit skill request.
- For natural routing, prefer naming the strongest intent cluster or natural trigger rather than a vague explanation.
- When a human-facing checkpoint, summary, verification result, or handoff is emitted, prefer an explicit route and next step when that action is not already obvious.
- For `vico-ground`, prefer the pair:
  - `Next route`
  - `Next action`
- Route literals should stay stable, especially:
  - `direct_execute`
  - `vico-plan`
  - `stay_in_ground`
  - `vico-plan -> vico-exec`

## Trigger Model

- Route Vico skills by intent cluster first, not by literal phrase match alone.
- Treat natural-language examples as strong hints, not as the only legal entrypoints.
- Use phrase lists to improve recall, especially for short colloquial requests, but do not let phrase matching override clearer intent signals.
- Apply route preconditions before locking a skill:
  - `vico-ground`: user is trying to orient, inspect, align, map, challenge, review, or build shared ground
  - `vico-plan`: user is trying to create, reconcile, verify, sync, replan, or close tracked work
  - `vico-exec`: user wants persistent implementation continuation and an active plan exists
  - `vico-feedback`: user is giving feedback about `vico-skills` behavior or asking to draft/file an issue about it
- Prefer one short clarification question when the same wording could reasonably map to more than one route.
- Prefer direct execution or direct answer when the request is clearly narrow, local, and does not benefit from Vico routing.
- Short colloquial repo-orientation phrases such as `scan`, `quick pass`, `orient me`, `扫一下`, `摸底`, `盘一下`, or `过一遍整体` should be treated as strong `vico-ground` hints when they target the whole repo, architecture, boundaries, or overall structure.
- Short colloquial tracked-work phrases such as `做个计划`, `收个口`, `对一下 plan`, `继续推进这个计划`, `verify 一下`, or `close 这个` should be treated as strong `vico-plan` hints when tracked work is already in scope.
- Short colloquial persistence phrases such as `继续做`, `一直做完`, `别停`, `接着跑`, or `继续直到完成` should be treated as strong `vico-exec` hints only when an active plan already exists.
- Short colloquial feedback phrases such as `提个 issue`, `记个反馈`, `这个体验别扭`, `这个触发不对`, or `帮我整理成 issue` should be treated as strong `vico-feedback` hints when they clearly target `vico-skills` itself.

## Workflow Re-entry Rule

- Workflow re-entry is a first-class supported path, not an exception path.
- Direct execution may happen before, during, or after tracked workflow.
- When tracked workflow resumes, the active Vico route should reconcile against current repository reality before trusting stale `.vico` state.

## Route Shift Policy

- Escalation and de-escalation are both valid workflow moves.
- If work grows beyond safe local execution, route into `vico-plan` or `vico-exec` as needed.
- If work shrinks back into a local, low-risk change, prefer `direct_execute` over keeping the user inside a heavier workflow.
- When re-entering tracked workflow after direct execution, perform the minimum reconcile or sync needed to align `.vico` state with current repository reality.

## Forward-Only Contract Discipline

- Default to forward design and assume no historical burden unless the user explicitly says compatibility matters.
- Do not preserve legacy names, aliases, modes, files, or structures by default.
- Prefer one clear contract over overlapping transitional surfaces.
- When an old surface is actively misleading, replace it instead of carrying an indefinite compatibility layer.
- Update owner sources first, then refresh derived forms, then remove the obsolete surface.

## Verification Authority

- `Status`, checklist completion, and index linkage are operational planning signals, not final proof of completion.
- Final close-out decisions should be gated by current repository evidence via `vico-plan verify`.

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
| Shared scripts | owner script file, currently under `vico-plan/scripts/` | skill-local wrapper entries under `<skill>/scripts/` when still needed | ensure owner source exists, local wrapper entry points exist where required, and runtime references do not point across skill boundaries |
| Shared status and decision rules | owner reference file, currently under `vico-plan/references/` | skill-local full reference copies where runtime visibility is required | ensure owner files exist, local copies exist where required, and copies are treated as derived content |
| Strong templates | owner template file, such as `plan-template.md`, `prd-template.md`, `reconcile-output-template.md` | skill-local visible copies or references needed for runtime closure | ensure owner templates exist, required local closures exist, and key structure remains stable |
| Feedback / issue templates | owner template file under `vico-feedback/references/` | issue drafts and filing behavior in `vico-feedback` | ensure draft templates exist, stay concise, and keep confirmation boundaries explicit |
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
