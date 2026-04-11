# Reconcile

Use this reference when `wilco-plan` needs to compare current docs against code and tests before rewriting the active plan.

## Checklist

### Plan Checks

- What phases exist?
- What acceptance criteria exist per phase?
- Which architectural decisions are supposed to be durable?
- What current status or progress markers are already in the plan?

### Optional PRD Checks

- What problem is the PRD trying to solve?
- What outcomes are explicitly in scope?
- What is explicitly out of scope?
- Does the active plan no longer carries enough durable scope, intent, or acceptance on its own?

### Code And Test Checks

- Are the intended entrypoints present?
- Are the relevant modules present, moved, or deleted?
- Are focused tests present near the logic?
- Do regression or flow tests indicate the behavior exists?
- Are there obvious TODO/FIXME notes that indicate unfinished work?

### Replacement Checks

- Does the current active slug still represent one clean execution contract?
- Is active overlap small enough to reuse the slug safely?
- Would replacing the current active docs with one fresh dated slug be simpler than preserving them? This is the `replace active slug` check.

## Classification Rules

- `done`: code and tests support the conclusion that the acceptance intent is implemented.
- `partial`: some of the intended behavior exists, but not enough to call complete.
- `not_started`: no meaningful implementation evidence exists yet.
- `diverged`: implementation exists, but the structure or behavior no longer matches the plan.
- `unclear`: available evidence is insufficient for a reliable conclusion.

## Output Template

```md
## Reconcile Summary

- Plan: in_progress / stale / missing
- PRD: active / accepted / stale / missing
- Alignment: aligned / partially_aligned / diverged
- Overall implementation status: done / partial / not_started / diverged / unclear
- Confidence: high / medium / low

## Verified Progress

- Phase 1: done / partial / not_started / diverged / unclear
- Phase 2: ...

## Evidence

- code paths checked
- tests checked
- key behaviors or architectural changes observed

## Divergences

- plan says X, code now does Y

## Recommended Next Step

- update existing active plan
- upgrade to `prd_backed` via `upgrade-to-prd-backed`
- replace active slug with one fresh dated slug
- or close out and delete active docs
```

Use this only when temporary reconcile state is actually needed. Prefer folding conclusions directly into the active plan.
