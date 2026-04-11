---
name: vico-exec
description: Execute the current Vico plan continuously until completion or a real blocker is reached. Use when the user wants the agent to keep going without stopping after each small step, carry out an active plan under `.vico/plans/active/` item by item, continue from temporary reconcile state when needed, keep going until complete, or follow a Ralph-like persistent execution loop. For Claude Code, this skill can be paired with bundled hooks; for Codex, use the same execute loop directly.
---

# Vico Exec

## Overview

Execute the current plan in a persistent loop:

1. reconcile current state
2. pick the smallest unblocked next step
3. implement it
4. verify it
5. update plan state
6. continue

Do not stop just because one small slice completed. Stop only when:

- the plan is complete
- a real blocker exists
- a user decision is required
- the current plan is stale enough that execution would be misleading

This skill owns implementation progress and plan synchronization, not final close-out deletion. When the work is truly complete, route to `vico-plan close`.

Treat natural requests such as `keep going`, `continue until complete`, `execute the active plan`, `carry this through unless blocked`, or `how do I use vico-exec` as valid `vico-exec` entrypoints when an active plan already exists.
If the user sounds like they want persistent execution but no active plan exists, ask a short clarification question or route them through `vico-plan` instead of guessing.

## Inputs

Accept either:

- an index manifest under `.vico/index/<slug>.json`
- an active plan under `.vico/plans/active/<slug>.md`
- or the current temporary reconcile file under `.vico/resume/<slug>.md`

Prefer the index manifest when present so cross-agent coordination does not rely on guessing file paths.
Prefer the plan as the long-lived execution anchor. Use temporary reconcile state only when a handoff or reconciliation snapshot is actually needed.
Treat the active plan as the primary execution anchor in both `plan_only` and `prd_backed` modes. In `prd_backed`, consult the PRD for scope and intent drift, but keep execution centered on the plan.

If the plan is stale, the current temporary reconcile state is stale, or the current implementation is unclear, route back through `vico-plan` for reconcile instead of exposing a separate resume step by default.
Treat direct-execution detours as normal: if execution resumes after out-of-band changes, reconcile against current repository reality before trusting the previous plan state.

## Multi-Active Safety Rules

- If more than one active slug exists and the intended execution target is not explicit, do not guess. Ask for an explicit slug or route back through `vico-plan review`.
- An explicit slug, a matching index manifest, or unambiguous current-turn user steering may select the execution target.
- If multiple active slugs remain materially plausible after inspection, stop and surface the ambiguity instead of starting execution on the wrong plan.

## Mode Contract

`vico-exec` should support these explicit modes:

- default
  - execute the current active plan
- `help`
  - show inputs, behavior, safety rules, and common examples

## Output Contract

For each meaningful execution pass:

- produce a compact execution report using [references/execution-report-template.md](references/execution-report-template.md)
- use the user's primary working language when it is clear from the conversation
- if the user's preferred language is unclear, mirror the user's most recent substantive message
- keep commands, status literals, blocker types, file paths, and other machine-meaningful literals stable unless that downstream contract is explicitly changed
- persist plan, index, or temporary reconcile updates to disk when the user expects docs to stay current or when continuation depends on accurate execution state
- do not fabricate disk writes when no execution-state change is needed
- route to `vico-plan close` automatically when implementation is complete and the user expects end-to-end completion
- include the active source, active slug, and continuation basis in the execution report so the user can see why execution continued or stopped
- keep deeper continuation heuristics implicit by default unless the user asks for execution internals or a blocker requires them to understand the exact boundary

## Execution Loop

Follow the loop in [references/execute-loop.md](references/execute-loop.md).

High-level rules:

- Always work from the smallest unblocked acceptance item or equivalent next slice.
- Do not drift into unrelated cleanup.
- Verify after each meaningful step.
- Update the plan as you go when the user wants execution-state docs kept current.
- If execution started from a temporary reconcile/handoff state, fold the important conclusions back into the plan as soon as the plan is current again.
- When execution is back in a clear steady state, prefer deleting the current temporary reconcile file or dropping it from the index rather than leaving stale handoff state behind.
- Prefer `scripts/sync_vico_index.py` for derived index refresh instead of hand-editing manifests.
- Persist execution-state changes to disk when they are needed to preserve continuity across turns or tools.
- When a blocker is real, say exactly why execution cannot continue and what decision or input is needed.
- Continue after each completed slice when another unblocked step exists.
- Do not stop merely because one checklist item finished.
- If the user intent is end-to-end completion and implementation is now complete, automatically route to `vico-plan close` rather than making the user remember that extra step.

For each execution pass, produce a compact execution report using [references/execution-report-template.md](references/execution-report-template.md).
When blocked, classify the blocker and use the blocked output shape in [references/blocker-taxonomy.md](references/blocker-taxonomy.md).

## Claude Code

For Claude Code, this skill can be paired with bundled hook scripts:

- [references/hooks-setup.md](references/hooks-setup.md)
- `scripts/session_start_hook.ps1`
- `scripts/stop_hook.ps1`

The hooks are optional but useful when you want to bias Claude toward continuing until the plan is actually complete or a real blocker is reached.

## Codex

Codex does not have equivalent event hooks. Use the same execute loop directly and rely on:

- this skill
- repository `AGENTS.md`
- explicit instruction to continue until complete or blocked

## References

- Use [references/execute-loop.md](references/execute-loop.md) for the step-by-step loop.
- Use [references/help-template.md](references/help-template.md) for `vico-exec help`.
- Use [references/execution-report-template.md](references/execution-report-template.md) for per-step output.
- Use [references/blocker-taxonomy.md](references/blocker-taxonomy.md) for blocker classification.
- Use [references/status-vocabulary.md](references/status-vocabulary.md) for shared status terms.
- Use [references/automation.md](references/automation.md) when refreshing index state.
- Use [references/hooks-setup.md](references/hooks-setup.md) for Claude Code hook wiring.
