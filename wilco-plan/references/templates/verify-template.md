# Verify Template

Use this shape for `wilco-plan verify`.
Render headings and prose in the user's primary working language when it is clear from the conversation.
Keep commands, verdict literals, status literals, and slug/path literals unchanged.

```md
## Plan Verify

- Selected slug: ...
- Completion verdict: `verified_complete` | `not_complete` | `ambiguous`
- Tracking mode: `plan_only` | `prd_backed`

## Evidence

- code evidence that supports or contradicts completion
- test or verification evidence that supports or contradicts completion

## Open Gaps

- unchecked or weakly-supported plan items
- stale docs or ambiguous completion claims

## Recommended Action

- `direct_execute`
- `wilco-plan`
- `wilco-plan -> wilco-exec`

## Recommended Next Mode

- `close`
- `verify close`
- `verify sync`
- `verify replan`
- `sync`
- `replan`
- `prd`
- `wilco-exec`
```

`verify` must be read-only. It should not rewrite plan state, update index metadata, or mutate active docs.
