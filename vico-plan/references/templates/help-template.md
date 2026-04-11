# Help Template

Use this shape for `vico-plan help`.
Render headings and prose in the user's primary working language when it is clear from the conversation.
Keep commands and mode literals unchanged.

```md
## Vico Plan Help

- Entry: `vico-plan`
- Default role: the only front door for tracked work
- Axis position: the tracked-execution front door; move from vibe execution into explicit tracked planning only when needed

## Modes

- default
- review
- verify
- sync
- prd
- replan
- replace
- truth
- close
- cancel

## Input Sources

- direct user input
- matching `vico-probe` handoff
- active plan / optional PRD
- current code and test state

## Input Precedence

1. explicit user input
2. matching `vico-probe` handoff
3. active plan / optional PRD
4. code reality

## Route Visibility

- show `Skill route` and `Route reason` in the first visible update when `vico-plan` is selected

## Safety Rules

- `review` is read-only
- `verify` is read-only
- `truth` is manual only
- `replace`, `close`, and `cancel` require explicit slug when multiple active slugs exist

## Mode Hints

- `sync`: use when code moved and the current plan should catch up
- `verify`: use when you need to check completion against real code and test evidence before close-out
- `verify close`: use when you want verification to gate an immediate close-out
- `verify sync`: use when you want verification to gate an immediate state refresh
- `verify replan`: use when you want verification to gate an immediate execution-contract rewrite
- `replan`: use when the same slug still applies, but the execution contract itself should be rewritten
- `prd`: use when the work now needs or updates `prd_backed` framing

## Examples

- `vico-plan`
- `vico-plan review`
- `vico-plan verify`
- `vico-plan verify sync`
- `vico-plan verify replan`
- `vico-plan sync`
- `vico-plan prd`
- `vico-plan replace`
- `vico-plan close`
- `vico-plan cancel`
```

Keep help compact and command-like. It should explain the controller clearly without restating the full skill contract.
