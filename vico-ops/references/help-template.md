# Help Template

Use this shape for `vico-ops help`.
Render headings and prose in the user's primary working language when it is clear from the conversation.
Keep commands and mode literals unchanged.

```md
## Vico Ops Help

- Entry: `vico-ops`
- Default role: repo-local maintenance for tracked Vico docs and lifecycle state
- Surface type: repo-local operations, not planning or execution

## Modes

- help
- bootstrap
- sync
- close
- cancel
- truth
- validate

## Routing Hints

- use `bootstrap` when tracked work needs its initial `.vico` artifact set
- use `sync` when active docs or derived state need to catch up to repository reality
- use `close` when tracked work is complete and active docs should be deleted
- use `cancel` when tracked work is abandoned and active docs should be deleted
- use `truth` when durable architecture truth should move into `docs/architecture/`
- use `validate` when the current `.vico` workspace needs schema / invariant checks
- if the real need is to shape or rewrite the execution contract, route to `vico-plan`
- if the real need is to verify completion against code and tests, route to `vico-plan verify`

## Safety Rules

- `close` and `cancel` are destructive
- require explicit slug selection for destructive actions when multiple active slugs exist
- prefer `vico-plan verify` before `close` when completion evidence is not already strong
- use repo-local owner sources under `runtime/cli/`

## Route Visibility

- `Skill route: vico-ops`
- `Route reason: <explicit_skill_request | intent_cluster | natural_trigger>`
- optional `Route detail: <repo_local_ops | lifecycle_action | exact trigger phrase>`
- optional `Route mode: <help | bootstrap | sync | close | cancel | truth | validate>`

## Examples

- `vico-ops help`
- `bootstrap a new slug`
- `sync the active docs`
- `close this tracked work`
- `cancel this slug`
- `extract architecture truth`
- `validate the vico workspace`
```

Keep help compact and operations-focused.
