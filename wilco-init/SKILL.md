---
name: wilco-init
description: Bootstrap new Wilco work by choosing a stable slug, deciding whether the task should stay no-doc, become plan-only, or escalate to PRD-backed tracking, and creating the minimal initial artifact set. Use when a new task is first entering `.wilco`, when the user wants to start a tracked slug cleanly, or when initial plan/PRD/index scaffolding should be created consistently.
---

# Wilco Init

## Overview

Start new tracked work without hand-building every file. This is the normal entrypoint for any new tracked slug. Use it to create the smallest correct Wilco footprint up front, then hand off to `wilco-plan` or `wilco-prd` for real content refinement.

## Workflow

1. Decide whether the task should remain `no-doc`, become `plan-only`, or be PRD-backed.
2. Choose one stable slug.
3. Create the minimal artifact set for that level.
4. Create the derived index linkage for every tracked slug.
5. Sync headers and minimal index linkage.
6. Hand off to `wilco-plan` or `wilco-prd` for real content refinement if needed.

## Rules

- Default to `plan-only`.
- Do not create a PRD just for symmetry.
- If the task is truly trivial and independent, keep it `no-doc`.
- If the task will be tracked, create an index manifest along with the primary tracked artifact set.
- Prefer `prd-plan-arch` only when architecture truth should exist immediately, not just eventually.

## Automation

Use `scripts/bootstrap_wilco_slug.py` to create the initial files, including the derived index manifest for tracked work, then use `../wilco-docs/scripts/sync_wilco_headers.py` or `../wilco-docs/scripts/sync_wilco_index.py` only if you need extra repair or follow-up normalization.

## References

- Use [references/bootstrap-levels.md](references/bootstrap-levels.md) for choosing the initial artifact level.
- Use `scripts/bootstrap_wilco_slug.py` for consistent file creation.
- Use `wilco-plan` when the new slug should immediately become a real execution plan.
- Use `wilco-prd` when the new slug needs scope clarification before execution.
