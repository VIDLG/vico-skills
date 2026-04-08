# Resume Output Template

Use this shape for a resume report.
Preserve these section headers exactly and keep status values within the shared Wilco vocabulary.

```md
## Resume Summary

- Manifest: optional `.wilco/index/<slug>.json`
- Resume file: `.wilco/resume/<slug>.md`
- PRD: active / accepted / stale / missing
- Plan: in_progress / partially_completed / stale / missing
- Alignment: aligned / partially_aligned / diverged
- Overall implementation status: done / partial / not_started / diverged / unclear
- Confidence: high / medium / low

Resume reports are current-state snapshots, not replacements for the plan.
Refresh the current resume file when stale; do not keep historical resume snapshots by default.
Delete the resume file or clear its index linkage once the plan is current again and no handoff or recovery need remains.

## Verified Progress

- Phase 1: done / partial / not_started / diverged / unclear
- Phase 2: ...

## Evidence

- code paths checked
- tests checked
- key behaviors or architectural changes observed
- evidence strong enough / incomplete

## Divergences

- plan says X, code now does Y
- PRD assumes A, implementation now assumes B

## Unresolved Areas

- questions that still need confirmation
- places where implementation evidence is insufficient

## Recommended Next Step

- the smallest correct next action to continue work

## Recommended Doc Updates

- update plan status
- update stale source links
- update PRD only if scope changed
- use `downgrade-to-plan-only` if the PRD no longer adds independent value
- record slug splits in both prose and index linkage if a new topic emerged
- extract architecture truth if needed
```

If the report contradicts the checklist, recommend updating the plan rather than letting the resume report become the only source of truth.
If no manifest exists, omit the `Manifest` line instead of inventing one just for symmetry.
