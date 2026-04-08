---
name: wilco-prd
description: Create a Wilco-style repo-local PRD through user interview, codebase exploration, and design clarification, then write it to `docs/prd/active/<slug>.md`. Use when the user wants to write a PRD, define a new engineering initiative, capture scope and acceptance criteria in-repo, or replace GitHub-issue-based PRD workflows with repository-native docs.
---

# Write Repo Prd

## Overview

Write PRDs as canonical repository documents, not GitHub issues. Use stable slugs, put dates and status in the document header, and align the result with the repo's `docs/` lifecycle.

## Workflow

1. Ask the user for the problem, goals, non-goals, constraints, and any solution ideas.
2. Explore the repo to verify assumptions and understand current architecture and ownership.
3. Interview the user until the scope, interfaces, and tradeoffs are clear enough to write a durable PRD.
4. Identify the main modules, boundaries, and testing expectations without locking in fragile file-level detail.
5. Choose a stable topic slug and target file path: `docs/prd/active/<slug>.md`.
6. Write the PRD using the repository template in [references/prd-template.md](references/prd-template.md).
7. If the repo's docs structure is unclear or needs normalization, also use `docs-governance`.

## Writing Rules

- Put metadata in the header, not in the file name.
- Use a stable slug for the file name.
- Do not default to GitHub issues or issue-body formatting.
- Capture implementation and testing decisions, but avoid file paths and code snippets that will rot quickly.
- Keep the PRD user-facing and decision-oriented; detailed execution belongs in the plan.

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
- Use `docs-governance` when you need help deciding slug, location, or lifecycle treatment.
