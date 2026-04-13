# Help Template

Use this shape for `vico-exec help`.
Render headings and prose in the user's primary working language when it is clear from the conversation.
Keep commands and mode literals unchanged.

```md
## Vico Exec Help

- Entry: `vico-exec`
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
- use the bundled Claude runner when hooks are not enough and you want a stronger repeat-until-stop loop
- when end-to-end completion is requested and implementation is complete, recommend `vico-plan verify` then `vico-ops close` rather than closing automatically
- show this route-debug shape in the first visible update when `vico-exec` is selected:
  - `Skill route: vico-exec`
  - `Route reason: <explicit_skill_request | intent_cluster | natural_trigger>`
  - optional `Route detail: <persistent_implementation | continue_until_complete | exact trigger phrase>`
  - optional `Route mode: <default | cc | help>`

## Modes

- default
- cc
- help

## Safety Rules

- do not perform close-out deletion directly; `vico-exec` may only recommend `vico-plan verify` or `vico-ops close`
- route back through `vico-plan` when execution state is unclear
- do not guess the execution target when multiple active slugs are plausible

## Examples

- `vico-exec`
- `继续做`
- `别停`
- `vico-exec cc`
- `run this with cc`
- `handoff to cc`
- `vico-exec help`
- `python3 vico-skills/vico-exec/scripts/claude_exec_runner.py --repo-root D:/projects/spoon`
```

Keep help compact and execution-focused.
