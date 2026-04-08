# Cleanup Output Template

Use this shape when `wilco-cleanup` performs or recommends close-out work.

Preserve these section headers exactly so later agents can scan the result quickly.

```md
## Cleanup Summary

- Slug: `<slug>`
- Outcome: archived / cancelled / superseded / partial_cleanup
- Confidence: high / medium / low

## Archive Actions

- plan: archived / left_active / missing
- prd: archived / left_active / missing
- archive targets: ...

## Temporary State Actions

- resume: deleted / kept / missing
- index: deleted / rewritten / refreshed / missing

## Architecture Follow-Up

- extracted now / already current / still needed
- target docs: ...

## Risks Or Follow-Up

- unresolved items that still block full close-out

## Recommended Next Step

- the smallest correct next action
```
