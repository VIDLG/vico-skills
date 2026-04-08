---
name: wilco-prd
description: Create a Wilco-style repo-local PRD through user interview, codebase exploration, and design clarification, then write it to `.wilco/prd/active/<slug>.md` when the work is large enough to justify a PRD. Use when the user wants to write a PRD, define a substantial engineering initiative, capture scope and acceptance criteria in-repo, or replace issue-based PRD workflows with repository-native planning docs. For smaller, clearer tasks, prefer plan-only workflows instead of forcing a PRD.
---

# Write Repo Prd

## Overview

Write PRDs as canonical repository documents, not GitHub issues. Use stable slugs, put dates and status in the document header, and align the result with the repo's `docs/` lifecycle.

Do not assume every task deserves a PRD.

## Workflow

1. Ask the user for the problem, goals, non-goals, constraints, and any solution ideas.
2. Explore the repo to verify assumptions and understand current architecture and ownership.
3. Decide whether the work is large enough to justify a PRD.
4. If the work is small, tightly scoped, and implementation-facing, recommend using `wilco-plan` directly instead of creating a PRD.
5. If the work deserves a PRD, interview the user until the scope, interfaces, and tradeoffs are clear enough to write a durable PRD.
6. Identify the main modules, boundaries, and testing expectations without locking in fragile file-level detail.
7. If `.wilco/` does not exist yet, initialize it as the Wilco planning workspace before writing any PRD files.
8. Choose a stable topic slug and target file path: `.wilco/prd/active/<slug>.md`.
9. Create or update `.wilco/index/<slug>.json` so PRD, plan, resume, and architecture links have a machine-readable coordination layer.
10. Write the PRD using the repository template in [references/prd-template.md](references/prd-template.md).
11. If the repo's docs structure is unclear or needs normalization, also use `wilco-docs`.

## Writing Rules

- Put metadata in the header, not in the file name.
- Use a stable slug for the file name.
- Do not default to GitHub issues or issue-body formatting.
- Capture implementation and testing decisions, but avoid file paths and code snippets that will rot quickly.
- Keep the PRD user-facing and decision-oriented; detailed execution belongs in the plan.
- Prefer PRDs for medium or large work, multi-phase work, or changes where intent and scope will outlive immediate implementation.

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
- Use `wilco-docs` when you need help deciding slug, location, or lifecycle treatment.
