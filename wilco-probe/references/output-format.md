# Wilco Probe Output Format

Use this file for examples. The normative rules live in `../SKILL.md`.

## Concise Question Template

```md
wilco-skills | workflow > lifecycle-transitions
Mode: concise | available: concise, detailed
Priority: critical

Question 7: Should this rule be enforced at the workflow layer?

Options
1. `Recommended` Yes, enforce it centrally.
2. No, keep it as guidance only.
```

## Cross-Topic Scheduling Example

```md
wilco-skills | workflow > slug-lifecycle
Mode: concise | available: concise, detailed
Priority: critical

Question 15: Should tracked slugs remain stable IDs?

Options
1. `Recommended` Yes, treat slug as a stable ID.
2. No, allow midstream renames.

---

wilco-skills | distribution > runtime-closure
Mode: concise | available: concise, detailed
Priority: critical

Question 16: Should runtime avoid cross-skill path dependencies?

Options
1. `Recommended` Yes, require skill-local runtime closure.
2. No, cross-skill paths are acceptable.
```

## Recommendation Shortcut Example

```md
wilco-skills | overlap-and-rebuild > historical-scope
Mode: concise | available: concise, detailed
Priority: important

Recommendation 18: Ignore historical slugs during overlap resolution by default.

Why now
- Historical slugs live in git and do not improve current execution clarity.

Write-back target
- .wilco/README.md
- wilco-plan/references/rules/routing.md
```

## Scan Example

```md
wilco-skills | wilco-probe > controller-gaps
Mode: concise | available: concise, detailed
Priority: critical

Intent overlay

- inspect current `wilco-probe` design for contract gaps

Findings

- default routing must remain controller-driven rather than always dropping into `grill`
- `grill` should stay a sustained-questioning submode rather than the default path
- handoff routing hints must stay aligned with `wilco-plan`

Evidence

- the contract already distinguishes `default`, `scan`, `grill`, `review`, and `resolve`
- `wilco-plan` already consumes `Target`, optional `Slug`, optional `Issue classes`, and the decision sections

Topic map snapshot

- mode-contract: active
- handoff-shape: active
- topic-map-controls: deferred
- validator-coverage: deferred

High-risk gaps

- examples and help can drift away from the contract if not kept current
- agent prompts and examples must keep reinforcing single-question defaults

Likely recommendations

- keep the default route evidence-first
- keep `grill` as an explicit sustained-questioning mode
- keep `Probe Handoff` aligned with `wilco-plan`

Open questions worth asking

- should `review` show the topic map by default or only when it adds value
- should long-lived probe sessions eventually expose a lightweight checkpoint command

Suggested next mode

- grill
```

## Review Example

```md
wilco-skills | wilco-probe > handoff-contract
Mode: concise | available: concise, detailed
Priority: important

Intent overlay

- checkpoint current probe state before changing the contract again

Accepted decisions

- `scan` should stay diagnostic rather than opening a long question chain.
- dominant low-risk choices may use direct recommendation.
- `Probe Handoff` should carry routing hints for `wilco-plan`.

Unresolved decisions

- whether `review` should show the topic map by default in long sessions

Deferred issues

- whether topic-map snapshots should appear by default in every `review`

Recommended resolutions

- prefer `resolve` to emit handoff when `wilco-plan` is the next consumer

Topic map snapshot

- handoff-shape: active
- output-modes: deferred
- validator-coverage: deferred

Suggested next mode

- resolve
```

## Grill Example

```md
wilco-skills | wilco-probe > routing-gaps
Mode: concise | available: concise, detailed
Priority: critical

Question 17: Should default `wilco-probe` ask immediately when `ask-user` issues remain, while reserving `grill` for sustained interrogation?

Options
1. `Recommended` Yes. Default probe should ask the single best question, and `grill` should mean a committed questioning loop.
2. No. Default probe should always drop into `grill` once any `ask-user` issue exists.

Accepted short replies
- `1`
- `1 do cont`
- `rec do`
```

## Object-Specific Topic Map Example

```md
Current working topic map for wilco-skills:

- workflow
- contract-map
- distribution
- sync-and-validation
- migration-execution
- template-contracts
- index-schema
- docs-governance
- probe-itself

Reason:
- this map was derived from the object's current workflow, contract, distribution, and governance structure
- it is not a universal topic taxonomy for every future probe target
```

## Candidate Ranking Example

```md
Top-level topic candidates after Question 15:

- workflow: important, but now mostly on downgrade mechanics
- distribution: critical, because runtime closure and validator hard-fail rules still change the install model
- contract-map: important, waiting on distribution decisions
- migration-execution: unvisited, so it receives an early coverage bonus

Next question chosen: distribution > runtime-closure
Reason: highest impact plus highest dependency unlock across the current topic map.
```

## Topic Coverage Example

```md
Top-level topic coverage:

- workflow: active
- contract-map: deferred
- distribution: active
- sync-and-validation: deferred
- migration-execution: unvisited
- template-contracts: unvisited
- index-schema: unvisited
- docs-governance: deferred
- probe-itself: deferred

Scheduler rule:
- if workflow has already taken 2 consecutive questions, compare the next best workflow candidate against the best unvisited topic candidate before asking another workflow question
```

## Topic Map Snapshot Example

```md
Topic map snapshot:

- active topic: distribution
- workflow: deferred
- contract-map: deferred
- distribution: active
- sync-and-validation: unvisited
- migration-execution: unvisited
- template-contracts: unvisited
- index-schema: unvisited
- docs-governance: unvisited
- probe-itself: deferred

Recent map changes:
- reprioritize: distribution moved above contract-map
- add: migration-execution
```

## User-Directed Topic Map Update Example

```md
Topic map snapshot:

- workflow: active
- lifecycle: deferred
- migration: unvisited
- validation: deferred

Requested change
- delete: validation
- add: overlap-resolution

Updated topic map:

- workflow: active
- lifecycle: deferred
- migration: unvisited
- overlap-resolution: unvisited

Scheduler effect:
- removed stale validation candidates
- created one new candidate under overlap-resolution
```

## Expanded Question Example

```md
wilco-skills | wilco-probe > stop-conditions
Mode: detailed | available: concise, detailed
Priority: critical

Question 12: Should probing stop once only wording polish remains?

Options
1. `Recommended` Yes, transition directly to the final summary.
2. No, continue until wording is also fully optimized.

Evidence
- The current rules require rigor but do not define a stop condition.
- Long probing chains degrade when they keep re-asking style-level questions.

Why it matters
Without an explicit stop rule, the probe either stops too early or drifts into low-value repetition.

Decision dependency
This builds on the earlier decision to prioritize critical and important branches before detail-level work.

Failure mode
If this is left undefined, the workflow turns into an endless review loop.

Counterargument
If the user explicitly wants line-level wording review, stopping here could feel premature.

Write-back target
- wilco-probe/SKILL.md
```

## Expanded Recommendation Example

```md
wilco-skills | wilco-probe > recommendation-shortcut
Mode: detailed | available: concise, detailed
Priority: important

Recommendation 19: Use a direct recommendation when repository evidence is strong and one option clearly dominates.

Evidence
- The current workflow already penalizes duplicate questioning and wording churn.
- Some decisions are effectively settled by repository evidence before the user is asked.

Why now
This removes low-value turns without weakening rigor on truly contested branches.

Counterargument
If used too aggressively, the probe could stop surfacing user preference on borderline questions.

Write-back target
- wilco-probe/SKILL.md
```

## Final Summary Example

```md
Accepted decisions
- The probe uses `Question N: <question text>` on one line.
- `Options`, `Evidence`, `Why it matters`, `Decision dependency`, and `Write-back target` are core sections.

Unresolved decisions
- None.

Recommended resolutions
- None.

Suggested edits
- Update `wilco-probe/SKILL.md` with the new output contract.
- Add `wilco-probe/references/output-format.md` for long examples.

Edit priority
1. Update the skill contract.
2. Add the example reference.
3. Tighten the validator.

Not covered in this pass
- Concrete validator field names.
```

## Probe Handoff Example

```md
## Probe Handoff

Target
- wilco-skills

Slug
- 2026-04-11-wilco-probe-contract

Issue classes
- intent
- execution

Accepted decisions
- `wilco-plan` is the only default front door.

Unresolved decisions
- None.

Suggested edits
- Rewrite `wilco-plan/SKILL.md` as the front-door orchestrator.
- Remove the old user-facing init / prd / resume entrypoints.

Edit priority
1. README and contracts
2. `wilco-plan`
3. validators and automation
```
