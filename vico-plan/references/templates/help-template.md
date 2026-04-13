# Help Template

Use this shape for `vico-plan help`.
Render headings and prose in the user's primary working language when it is clear from the conversation.
Keep commands and mode literals unchanged.

```md
## Vico Plan Help

- Entry: `vico-plan`
- Default role: the default front door for tracked work
- Axis position: the tracked-execution front door; move from vibe execution into explicit tracked planning only when needed

## Modes

- default
- review
- verify
- prd
- replan

## Input Sources

- direct user input
- matching `vico-ground` handoff
- active plan / optional PRD
- current code and test state

## Input Precedence

1. explicit user input
2. matching `vico-ground` handoff
3. active plan / optional PRD
4. code reality

## Route Visibility

- show this route-debug shape in the first visible update when `vico-plan` is selected:
  - `Skill route: vico-plan`
  - `Route reason: <explicit_skill_request | intent_cluster | natural_trigger>`
  - optional `Route detail: <tracked_work_controller | verify_request | exact trigger phrase>`
  - optional `Route mode: <review | verify | prd | replan>`

## Safety Rules

- `review` is read-only
- `verify` is read-only
- route lifecycle and repo-local maintenance operations through `vico-ops`

## Mode Hints

- `verify`: use when you need to check completion against real code and test evidence before lifecycle cleanup
- `replan`: use when the same slug still applies, but the execution contract itself should be rewritten
- `prd`: use when the work now needs or updates `prd_backed` framing
- `vico-ops`: use after planning when the real need is bootstrap, sync, close, cancel, truth extraction, or workspace validation

## Examples

- `vico-plan`
- `做个计划`
- `对一下 plan`
- `vico-plan review`
- `vico-plan verify`
- `verify 一下`
- `vico-plan prd`
- `vico-plan replan`
- `vico-ops sync`
- `vico-ops close`
```

Keep help compact and command-like. It should explain the controller clearly without restating the full skill contract.
