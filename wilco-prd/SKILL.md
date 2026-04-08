---
name: wilco-prd
description: Create a Wilco-style repo-local PRD through user interview, codebase exploration, and design clarification, then write it under `.wilco/prd/active/` when the work is large enough to justify a PRD. Use when the user wants to write a PRD, define a substantial engineering initiative, capture scope and acceptance criteria in-repo, or replace issue-based PRD workflows with repository-native planning docs. For smaller, clearer tasks, prefer plan-only workflows instead of forcing a PRD.
---

# Write Repo Prd

## Overview

Write PRDs as canonical repository documents, not GitHub issues. Use stable slugs, put dates and status in the document header, and align the result with the repo's `docs/` lifecycle.

Do not assume every task deserves a PRD.

Before creating a new PRD, check whether the work already hits an active slug. Sometimes the right action is to update an existing PRD because scope moved, not to mint a new one.
Prefer plan-only unless there is a real need to preserve user-facing intent, scope, or acceptance outside the plan.
Do not treat this skill as the normal bootstrap entrypoint for new tracked work. If a new tracked slug does not exist yet, use `wilco-init` first.
This skill also owns the decision about whether an active PRD should remain active at all.

## Workflow

1. Ask the user for the problem, goals, non-goals, constraints, and any solution ideas.
2. Explore the repo to verify assumptions and understand current architecture and ownership.
3. Determine whether the work hits an existing active slug.
4. Decide whether the work is large enough to justify a PRD.
5. If the work is small, tightly scoped, and implementation-facing with no need to redefine scope, stop and route to `wilco-plan` directly instead of creating a PRD.
6. If an existing slug is hit and scope, goals, non-goals, or acceptance have changed, update that existing PRD rather than creating a sibling slug.
7. If an existing active PRD no longer provides independent scope, intent, or acceptance value beyond the plan, perform `downgrade-to-plan-only`:
   - confirm the downgrade is justified
   - move any still-useful execution detail into the plan
   - move any durable truth into architecture docs if needed
   - archive or retire the PRD instead of deleting it without trace
   - coordinate atomic updates to the plan, PRD state, headers, and index linkage
8. If no active slug is hit and the work should become tracked, hand off to `wilco-init` for slug bootstrap before writing the PRD.
9. If the work deserves a PRD, interview the user until the scope, interfaces, and tradeoffs are clear enough to write a durable PRD.
10. Identify the main modules, boundaries, and testing expectations without locking in fragile file-level detail.
11. Choose the stable topic slug and target file path: `.wilco/prd/active/<slug>.md`.
12. Update `.wilco/index/<slug>.json` only as a derived coordination layer for linked artifacts. Prefer `../wilco-docs/scripts/sync_wilco_index.py` when available instead of hand-editing derived linkage.
13. Write or update the PRD using the repository template in [references/prd-template.md](references/prd-template.md).
14. If the repo's docs structure is unclear or needs normalization, also use `wilco-docs`.

## Writing Rules

- Put metadata in the header, not in the file name.
- Use a stable slug for the file name.
- Do not default to GitHub issues or issue-body formatting.
- Capture implementation and testing decisions, but avoid file paths and code snippets that will rot quickly.
- Keep the PRD user-facing and decision-oriented; detailed execution belongs in the plan.
- Prefer PRDs for medium or large work, multi-phase work, or changes where intent and scope will outlive immediate implementation.
- Treat PRD creation as a hard escalation gate, not a polite suggestion. If the work does not justify a PRD, route back to the plan workflow.
- Treat `downgrade-to-plan-only` as an equally explicit lifecycle action. Do not keep a stale PRD active just because one once existed.
- Do not create a new PRD just because implementation diverged; first decide whether the divergence changed scope or only execution details.
- If tracked work changes only implementation progress, leave the PRD alone and update the plan instead.
- If tracked work changes goals, non-goals, success conditions, or product boundaries, update the PRD and keep the slug stable.
- If downgrading to plan-only, archive or explicitly retire the PRD; do not delete it without a traceable exit.
- If the plan already carries enough context for a small task, do not backfill a PRD just for process symmetry.

## Output Contract

Write PRDs with at least:

- `Status`
- `Created`
- `Updated`
- optional `Related plan`
- Problem Statement
- Solution
- User Stories
- Implementation Decisions
- Testing Decisions
- Out of Scope
- Further Notes

## References

- Use [references/prd-template.md](references/prd-template.md) for the repository PRD template.
- Use `.wilco/index/<slug>.json` as the machine-readable linkage file for cross-agent coordination.
- Use [../wilco-docs/references/automation.md](../wilco-docs/references/automation.md) when syncing derived index metadata.
- Use `wilco-init` when a slug does not exist yet and the task first needs to enter `.wilco`.
- Use `wilco-docs` when you need help deciding slug, location, or lifecycle treatment.
