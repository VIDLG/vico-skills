# Review Template

Use this shape for `wilco-plan review`.
Render headings and prose in the user's primary working language when it is clear from the conversation.
Keep commands, mode literals, status literals, and slug/path literals unchanged.

```md
## Plan Review

- Active slug(s): ...
- Selected slug: ...
- Tracking mode: `plan_only` | `prd_backed`
- Current progress: `not_started` | `partially_completed` | `mostly_complete` | `done`
- Drift risk: low | medium | high

## Current State

- latest known phase or execution slice
- whether plan appears ahead of code or behind code
- whether active overlap exists

## Recommended Next Step

- continue with current plan
- sync the plan to current code
- replan the current slug
- replace the active slug
- upgrade to `prd_backed`
- mark as `done` or `cancel`
```

`review` must be read-only. It should not rewrite plan state, update index metadata, or mutate active docs.
