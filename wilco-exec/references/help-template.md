# Help Template

Use this shape for `wilco-exec help`.
Render headings and prose in the user's primary working language when it is clear from the conversation.
Keep commands and mode literals unchanged.

```md
## Wilco Exec Help

- Entry: `wilco-exec`
- Default role: execute the current active plan
- Axis position: the heavy end of the execution axis; use only when an active plan already exists and persistent execution is wanted

## Inputs

- active plan
- optional index manifest
- optional temporary reconcile state

## Behavior

- execute the smallest unblocked next step
- verify after each meaningful step
- keep the plan current while executing
- route to `wilco-plan done` when end-to-end completion is requested
- show `Skill route` and `Route reason` in the first visible update when `wilco-exec` is selected

## Safety Rules

- do not perform close-out deletion directly
- route back through `wilco-plan` when execution state is unclear
- do not guess the execution target when multiple active slugs are plausible

## Examples

- `wilco-exec`
- `wilco-exec help`
```

Keep help compact and execution-focused.
