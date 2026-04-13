# Execution Report Template

Use this shape after each meaningful execution pass.
Render headings and prose in the user's primary working language when it is clear from the conversation.
Keep commands, status literals, blocker types, and path literals unchanged.

```md
## Execution Step

- Target: Phase 2 / acceptance criterion 3
- Reason: smallest unblocked remaining step

## Execution State

- Source: `index` | `plan` | `resume`
- Active slug: `...`
- Continuation basis: `continue` | `blocked` | `complete`
- Multi-active status: `single` | `explicit_slug` | `ambiguous`
- Confidence: high | medium | low
- Scope impact: local | active_slug | cross_slug | repo_wide
- Uncertainty source: weak verification | stale plan | blocker ambiguity | environment drift

## Changes

- code/doc changes made

## Verification

- commands or checks run
- result

## Plan Update

- checklist items updated
- `Updated` date changed or not
- divergence note added or not

## Next Step

- the next smallest unblocked action

## Risk If Skipped

- what worsens if the preferred next step is delayed or ignored

## Alternative Next Steps

- optional backup actions if the preferred next step is deferred or blocked
```
