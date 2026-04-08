---
name: wilco-execute
description: Execute the current Wilco plan continuously until completion or a real blocker is reached. Use when the user wants the agent to keep going without stopping after each small step, carry out an active plan under `.wilco/plans/active/` item by item, continue from a `wilco-resume` report, or follow a Ralph-like persistent execution loop. For Claude Code, this skill can be paired with bundled hooks; for Codex, use the same execute loop directly.
---

# Wilco Execute

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

Treat `wilco-resume` input as temporary handoff state, not as a permanent peer to the plan.
This skill owns implementation progress and plan synchronization, not final archive handling. When the work is truly complete, route to `wilco-cleanup` for `close-archive`.

## Inputs

Accept either:

- an index manifest under `.wilco/index/<slug>.json`
- an active plan under `.wilco/plans/active/<slug>.md`
- or the current resume file under `.wilco/resume/<slug>.md`

Prefer the index manifest when present so cross-agent coordination does not rely on guessing file paths.
Prefer the plan as the long-lived execution anchor. Use resume only when a handoff or reconciliation snapshot is actually needed.

If the plan is stale, the current resume is stale, or the current implementation is unclear, use `wilco-resume` first.

## Execution Loop

Follow the loop in [references/execute-loop.md](references/execute-loop.md).

High-level rules:

- Always work from the smallest unblocked acceptance item or equivalent next slice.
- Do not drift into unrelated cleanup.
- Verify after each meaningful step.
- Update the plan as you go when the user wants execution-state docs kept current.
- If execution started from a resume file, fold the important conclusions back into the plan as soon as the plan is current again.
- When execution is back in a clear steady state, prefer deleting the current resume file or dropping it from the index rather than leaving stale handoff state behind.
- Prefer `../wilco-docs/scripts/sync_wilco_index.py` for derived index refresh instead of hand-editing manifests.
- When a blocker is real, say exactly why execution cannot continue and what decision or input is needed.
- Continue after each completed slice when another unblocked step exists.
- Do not stop merely because one checklist item finished.
- If the user intent is end-to-end completion and implementation is now done, automatically route to `wilco-cleanup` rather than making the user remember that extra step.

For each execution pass, produce a compact execution report using [references/execution-report-template.md](references/execution-report-template.md).
When blocked, classify the blocker using [references/blocker-taxonomy.md](references/blocker-taxonomy.md).

## Claude Code

For Claude Code, this skill can be paired with bundled hook scripts:

- [references/hooks-setup.md](references/hooks-setup.md)
- `scripts/session_start_hook.ps1`
- `scripts/stop_hook.ps1`

The hooks are optional but useful when you want to bias Claude toward continuing until the plan is actually done or a real blocker is reached.

## Codex

Codex does not have equivalent event hooks. Use the same execute loop directly and rely on:

- this skill
- repository `AGENTS.md`
- explicit instruction to continue until done or blocked

## References

- Use [references/execute-loop.md](references/execute-loop.md) for the step-by-step loop.
- Use [references/execution-report-template.md](references/execution-report-template.md) for per-step output.
- Use [references/blocker-taxonomy.md](references/blocker-taxonomy.md) for blocker classification.
- Use [../wilco-docs/references/status-vocabulary.md](../wilco-docs/references/status-vocabulary.md) for shared status terms.
- Use [../wilco-docs/references/automation.md](../wilco-docs/references/automation.md) when refreshing index state.
- Use [references/hooks-setup.md](references/hooks-setup.md) for Claude Code hook wiring.
