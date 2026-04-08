# Wilco Grill Output Format

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

## Cross-Branch Scheduling Example

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

## Object-Specific Branch Map Example

```md
Current working branch map for wilco-skills:

- workflow
- contract-map
- distribution
- sync-and-validation
- migration-execution
- template-contracts
- index-schema
- docs-governance
- grill-itself

Reason:
- this map was derived from the object's current workflow, contract, distribution, and governance structure
- it is not a universal branch taxonomy for every future grill target
```

## Candidate Ranking Example

```md
Top-level branch candidates after Question 15:

- workflow: important, but now mostly on downgrade mechanics
- distribution: critical, because runtime closure still changes the install model
- contract-map: important, waiting on distribution decisions
- migration-execution: unvisited, so it receives an early coverage bonus

Next question chosen: distribution > runtime-closure
Reason: highest impact plus highest dependency unlock across the current branch map.
```

## Branch Coverage Example

```md
Top-level branch coverage:

- workflow: active
- contract-map: deferred
- distribution: active
- sync-and-validation: deferred
- migration-execution: unvisited
- template-contracts: unvisited
- index-schema: unvisited
- docs-governance: deferred
- grill-itself: deferred

Scheduler rule:
- if workflow has already taken 2 consecutive questions, compare the next best workflow candidate against the best unvisited branch candidate before asking another workflow question
```

## Branch Map Snapshot Example

```md
Branch map snapshot:

- active branch: distribution
- workflow: deferred
- contract-map: deferred
- distribution: active
- sync-and-validation: unvisited
- migration-execution: unvisited
- template-contracts: unvisited
- index-schema: unvisited
- docs-governance: unvisited
- grill-itself: deferred

Recent map changes:
- reprioritize: distribution moved above contract-map
- add: migration-execution
```

## Expanded Question Example

```md
wilco-skills | wilco-grill > stop-conditions
Mode: detailed | available: concise, detailed
Priority: critical

Question 12: Should grilling stop once only wording polish remains?

Options
1. `Recommended` Yes, transition directly to the final summary.
2. No, continue until wording is also fully optimized.

Evidence
- The current rules require rigor but do not define a stop condition.
- Long grilling chains degrade when they keep re-asking style-level questions.

Why it matters
Without an explicit stop rule, the grill either stops too early or drifts into low-value repetition.

Decision dependency
This builds on the earlier decision to prioritize critical and important branches before detail-level work.

Failure mode
If this is left undefined, the workflow turns into an endless review loop.

Counterargument
If the user explicitly wants line-level wording review, stopping here could feel premature.

Write-back target
- wilco-grill/SKILL.md
```

## Final Summary Example

```md
Accepted decisions
- The grill uses `Question N: <question text>` on one line.
- `Options`, `Evidence`, `Why it matters`, `Decision dependency`, and `Write-back target` are core sections.

Unresolved decisions
- None.

Recommended resolutions
- None.

Suggested edits
- Update `wilco-grill/SKILL.md` with the new output contract.
- Add `wilco-grill/references/output-format.md` for long examples.

Edit priority
1. Update the skill contract.
2. Add the example reference.
3. Tighten the validator.

Not covered in this pass
- Concrete validator field names.
```
