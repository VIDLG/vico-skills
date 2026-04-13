# Help Template

Use this shape for `vico-ground help`.
Render headings and prose in the user's primary working language when it is clear from the conversation.
Keep commands and move literals unchanged.

```md
## Vico Ground Help

- Entry: `vico-ground`
- Default role: build just enough shared ground to choose a safe next route
- Default posture: stay light, stop once the next route is clear

## Public Moves

- `scan`
- `clarify`
- `stress`
- `handoff`
- `help`

## Routing Hints

- use `scan` when facts are weak
- use `clarify` when scope, terms, or intent are weak
- use `stress` when a proposal, assumption, or plan needs pressure
- use `handoff` when the next route is already clear
- show this route-debug shape in the first visible update:
  - `Skill route: vico-ground`
  - `Route reason: <explicit_skill_request | intent_cluster | natural_trigger>`
  - optional `Route detail: <repo_orientation | architecture_scan | exact trigger phrase>`
  - optional `Route mode: <scan | clarify | stress | handoff>`

## Output

- `Move: <move>`
- `Conclusion`
- `Evidence`
- `Next route`
- `Next action`

## Examples

- `vico-ground`
- `vico-ground scan`
- `scan the repo`
- `扫一下这个项目`
- `vico-ground clarify`
- `vico-ground stress`
- `vico-ground handoff`
- `how do I use vico-ground`
```

Keep help compact and move-oriented.
