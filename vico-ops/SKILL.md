---
name: vico-ops
description: Repo-local operations surface for tracked Vico maintenance. Use when the user wants to bootstrap tracked docs, sync stale `.vico` state, close or cancel tracked work, extract durable truth, or validate the current Vico workspace.
---

# Vico Ops

`vico-ops` is the repo-local maintenance surface in Vico.

Use it for operations on tracked Vico artifacts and lifecycle state, not for problem framing or persistent implementation.
Keep repo-local automation owner sources under `runtime/cli/`; this skill is the user-facing control surface for those operations.

Treat natural requests such as `bootstrap a new slug`, `sync the active docs`, `close this tracked work`, `cancel this slug`, `extract architecture truth`, `validate the vico workspace`, or `how do I use vico-ops` as valid `vico-ops` entrypoints even when the user does not name the skill explicitly.

If the user's real intent is to shape or rewrite the execution contract itself, prefer `vico-plan`.
If the user's real intent is to verify completion against code reality, prefer `vico-plan verify` before `vico-ops close`.

## Agent Summary

- `Display name`: `Vico Ops`
- `Short description`: `Maintain tracked Vico docs and repo-local workflow state`
- `Default prompt`: `Act as the repo-local operations surface for Vico. Use runtime/cli owner sources to bootstrap tracked docs, sync stale .vico state, close or cancel tracked work, extract durable truth, or validate the current workspace. Keep operations explicit, prefer the smallest safe mutation, require explicit slug selection for destructive actions when multiple active slugs exist, and route back to vico-plan when the real need is planning or verification rather than maintenance.`

## Modes

- `help`
  - show the maintenance surface and common examples
- `bootstrap`
  - create the smallest valid tracked artifact set for new work
- `sync`
  - align active docs and derived state with current repository reality
- `close`
  - delete active docs for completed tracked work after verification is already strong enough
- `cancel`
  - delete active docs for abandoned tracked work
- `truth`
  - extract durable truth into `docs/architecture/`
- `validate`
  - validate the current `.vico` workspace

## Control Rules

- Prefer `vico-plan verify` before `close` when completion evidence is not already strong in the current turn.
- Prefer `vico-plan` over `vico-ops` when the execution contract itself needs to be created or rewritten.
- Prefer `vico-ops` over `vico-plan` when the plan already exists and the task is now maintenance, cleanup, or state alignment.
- Keep destructive operations explicit and target-aware.

## Multi-Active Safety Rules

- If more than one active slug exists, destructive modes require an explicit slug:
  - `close`
  - `cancel`
- `sync` should also prefer explicit slug selection when multiple active slugs are materially plausible.
- Do not guess a destructive target from loose context when multiple active slugs exist.

## Repo-Local Operations

Use repo-local owner sources under `runtime/cli/` for:

- bootstrap
- sync
- close
- cancel
- truth
- validate

Treat skill-local `vico-plan/scripts/` wrapper paths as compatibility command paths, not as owner sources.

## Output Contract

For user-facing output:

- use the user's primary working language when it is clear from the conversation
- keep mode names, path literals, and machine-facing fields stable
- surface this route-debug shape in the first visible update when `vico-ops` is selected:
  - `Skill route: vico-ops`
  - `Route reason: <explicit_skill_request | intent_cluster | natural_trigger>`
  - optional `Route detail: <repo_local_ops | lifecycle_action | exact trigger phrase>`
  - optional `Route mode: <help | bootstrap | sync | close | cancel | truth | validate>`

For destructive modes:

- show the selected slug
- show the operation reason
- show the affected artifacts

For `validate`:

- show whether the workspace passed
- show the failing artifacts or invariants when it does not

## References

- Use [references/help-template.md](references/help-template.md) for `vico-ops help`.
- Use repo-local owner sources under `runtime/cli/` for the actual maintenance operations.
