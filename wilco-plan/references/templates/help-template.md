# Help Template

Use this shape for `wilco-plan help`.
Render headings and prose in the user's primary working language when it is clear from the conversation.
Keep commands and mode literals unchanged.

```md
## Wilco Plan Help

- Entry: `wilco-plan`
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
- done
- cancel

## Input Sources

- direct user input
- matching `wilco-probe` handoff
- active plan / optional PRD
- current code and test state

## Input Precedence

1. explicit user input
2. matching `wilco-probe` handoff
3. active plan / optional PRD
4. code reality

## Route Visibility

- show `Skill route` and `Route reason` in the first visible update when `wilco-plan` is selected

## Safety Rules

- `review` is read-only
- `verify` is read-only
- `truth` is manual only
- `replace`, `done`, and `cancel` require explicit slug when multiple active slugs exist

## Mode Hints

- `sync`: use when code moved and the current plan should catch up
- `verify`: use when you need to check completion against real code and test evidence before close-out
- `replan`: use when the same slug still applies, but the execution contract itself should be rewritten
- `prd`: use when the work now needs or updates `prd_backed` framing

## Examples

- `wilco-plan`
- `wilco-plan review`
- `wilco-plan verify`
- `wilco-plan sync`
- `wilco-plan prd`
- `wilco-plan replace`
- `wilco-plan done`
- `wilco-plan cancel`
```

Keep help compact and command-like. It should explain the controller clearly without restating the full skill contract.
