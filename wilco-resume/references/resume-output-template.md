# Resume Output Template

Use this shape for a resume report.

```md
## Resume Summary

- PRD: active / accepted / stale / missing
- Plan: in_progress / partially_completed / stale / missing
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
- extract architecture truth if needed
```
