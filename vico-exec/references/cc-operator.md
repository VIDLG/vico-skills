# CC Operator Guide

Use this guide when `vico-exec cc` is driving Claude Code through the runner loop.

## When To Use `vico-exec cc`

Use `vico-exec cc` when:

- an active plan already exists
- Claude Code is the execution agent
- hooks are too weak to keep execution moving
- you want explicit outer-loop control over `continue`, `done`, `blocked`, `needs_user`, or `stale_plan`

Do not use `vico-exec cc` when:

- no active plan exists yet
- the next missing condition is still shared-ground work rather than execution
- the plan is obviously stale enough that `vico-plan` should run first

## Exit Codes

- `0`
  - `done`
- `2`
  - `blocked`
- `3`
  - `needs_user`
- `4`
  - `stale_plan`

## Recommended Operator Flow

1. ensure one active plan is clearly in scope
2. run `vico-exec cc`
3. if exit code is `0`, prefer `vico-plan verify` or `vico-plan close`
4. if exit code is `2`, inspect the blocker and decide whether to unblock or pause
5. if exit code is `3`, answer the pending user decision and rerun
6. if exit code is `4`, route back through `vico-plan`

## Hook Vs Runner

| Option | Best for | Weakness |
| --- | --- | --- |
| hooks | lightweight execution pressure inside a normal Claude session | weaker outer-loop control |
| runner | repeat-until-stop execution with explicit machine-readable stop reasons | heavier operator surface |

Choose hooks when you mainly want a reminder not to stop too early.
Choose the runner when you want deterministic outer-loop control and explicit stop states.

## Example Outcomes

### Example: `done`

- implementation and focused verification both passed
- next operator action: `vico-plan verify` or `vico-plan close`

### Example: `blocked`

- a real external blocker exists
- next operator action: inspect the blocker summary and unblock or pause

### Example: `needs_user`

- the agent reached a real user decision
- next operator action: answer the decision and rerun

### Example: `stale_plan`

- the plan no longer gives a safe execution contract
- next operator action: route back through `vico-plan`

## Good Defaults

- start with the repo-local plan already reconciled
- prefer a narrower slug when more than one active plan exists
- prefer `acceptEdits` or a similarly scoped permission mode instead of broad bypass modes
- keep the runner non-destructive; let `vico-plan close` handle close-out deletion
