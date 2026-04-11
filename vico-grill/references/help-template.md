# Help Template

Use this shape for `vico-grill help`.
Render headings and prose in the user's primary working language when it is clear from the conversation.
Keep commands and route literals unchanged.

```md
## Vico Grill Help

- Entry: `vico-grill`
- Default role: freeform sustained questioning for ideas, decisions, and tradeoffs
- Axis position: the freeform questioning lane; stay session-only until repository reality or tracked execution actually matters

## Behavior

- keep one active question at a time
- challenge assumptions and expose hidden constraints
- surface `Skill route` and `Route reason` in the first visible update when `vico-grill` is selected
- stay session-local by default
- do not pretend freeform conclusions are repository-backed findings
- if the user points at a concrete repo plan, PRD, design, codebase, slug, or `.vico` artifact, do not stay in `vico-grill`
- route to `vico-probe` when repository evidence should drive the next question
- route to `vico-plan` when the topic is already ready to become tracked work

## Shortcuts

- `推` / `rec`: choose the recommended option
- `继续` / `cont`: continue grilling
- `收口` / `close`: stop questioning and synthesize
- `probe`: upgrade to `vico-probe`
- `plan`: upgrade to `vico-plan`

## Examples

- `vico-grill`
- `grill this idea`
- `grill this problem`
- `stress-test this decision`
- `deep interview this tradeoff`
- `discuss this tradeoff`
- `how do I use vico-grill`
```

Keep help compact and pressure-focused.
