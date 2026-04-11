# Help Template

Use this shape for `wilco-probe help`.
Render headings and prose in the user's primary working language when it is clear from the conversation.
Keep commands and mode literals unchanged.

```md
## Wilco Probe Help

- Entry: `wilco-probe`
- Default role: inspect a plan, design, or codebase before planning
- Axis position: the probing axis; increase inspection intensity without turning every task into tracked execution
- Default behavior: do a light scan first, then route into recommendation, one question, review, grill, or resolve

## Modes

- default
- scan
- grill
- review
- resolve
- help

## Input Model

- user steering decides direction and priority
- repository evidence decides factual reality
- current probe state preserves continuity

## Internal State

- Intent Overlay
- Evidence Bank
- Issue Bank
- Topic Map
- Handoff State

## Behavior

- derive issues from evidence before asking the user
- surface `Skill route` and `Route reason` in the first visible update when `wilco-probe` is selected
- default to evidence-first probing
- route by issue state instead of forcing questioning every time
- surface `Skill route` and `Route reason` in the first visible update when `wilco-probe` is selected
- bootstrap a light scan when explicit `grill`, `review`, or `resolve` is invoked without usable current probe state
- enter `grill` when the next best action is sustained questioning
- allow a brief solve-and-return inside `grill` for bounded low-risk issues
- accept short action modifiers in `grill`, such as `推/rec`, `做/do`, `留/hold`, `继续/cont`, and `收口/close`
- allow direct recommendation when one option clearly dominates
- maintain an explicit topic map
- treat the topic map as a scheduler view derived from the issue bank
- keep internal probe state session-local by default
- emit a `Probe Handoff` block for `wilco-plan`

## Plan Targets

- `grill plan`: grill the current active plan as the target object
- `grill <slug>`: grill a specific tracked plan when multiple active slugs exist
- when the target is a plan, bounded low-risk clarifications may directly refine plan text before continuing `grill`

## Topic Map Controls

- show
- add
- delete
- split
- merge
- retire
- reprioritize

## Grill Shortcuts

- `推` / `rec`: choose the recommended option
- `做` / `do`: apply immediately
- `留` / `hold`: decide now without applying
- `继续` / `cont`: continue `grill`
- `收口` / `close`: stop questioning and synthesize

## Examples

- `wilco-probe`
- `wilco-probe scan`
- `wilco-probe grill`
- `wilco-probe grill plan`
- `wilco-probe review`
- `wilco-probe resolve`
- `wilco-probe help`
```

Keep help compact and decision-focused.
