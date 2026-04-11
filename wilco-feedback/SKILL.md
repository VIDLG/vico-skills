---
name: wilco-feedback
description: Turn user feedback about wilco-skills into a GitHub issue draft, check for likely duplicates when useful, and create the issue only after explicit user confirmation. Use when the user wants to report a bug, suggest a feature, describe workflow friction, complain about naming or UX, or ask to file an issue against wilco-skills.
---

# Wilco Feedback

Turn user feedback about `wilco-skills` into structured GitHub issues.

Treat natural requests such as `file an issue`, `report a bug`, `this workflow feels awkward`, `I have feedback about wilco-skills`, `draft a GitHub issue`, or `how do I use wilco-feedback` as valid `wilco-feedback` entrypoints even when the user does not name the skill explicitly.

## Goals

- capture user feedback in a structured form
- distinguish bugs, UX friction, contract inconsistencies, and feature requests
- draft a GitHub issue before creating it
- only create the issue after explicit user confirmation

## Inputs

- direct user feedback in the current turn
- current conversation context about the affected `wilco-skills` behavior
- repository evidence when local files or contracts help sharpen the report
- optional GitHub issue search results when de-duplication is useful

## Workflow

1. Identify the feedback type:
   - `bug`
   - `ux_friction`
   - `contract_gap`
   - `feature_request`
   Default to automatic classification from the user's wording and the current conversation context; do not force the user to choose a type up front unless the category is genuinely ambiguous.
2. Extract the minimum useful issue fields:
   - title
   - affected skill(s)
   - current behavior
   - expected behavior
   - why it matters
   - optional proposed direction
3. If key issue fields are missing, ask only the shortest clarifying question needed to complete the draft.
4. When useful, check for likely duplicates before filing.
   - when a likely duplicate is still open, prefer commenting or linking instead of opening a fresh issue
   - when a likely duplicate is closed but still clearly represents the same active problem, prefer suggesting `reopen`
5. Produce an issue draft using [references/issue-template.md](references/issue-template.md).
6. Do not create the GitHub issue until the user explicitly confirms with wording such as:
   - `create it`
   - `file it`
   - `open the issue`
   - `reopen it`
   - `comment there`
7. If the user confirms creation, create the issue with `gh issue create` against `VIDLG/wilco-skills`.
8. If the user confirms a duplicate-aware action:
   - reopen the matching issue with `gh issue reopen`
   - or add context with `gh issue comment`

## Safety Rules

- default to draft-only behavior
- do not create or edit GitHub issues without explicit user confirmation
- if `gh` authentication is missing or creation fails, return the draft and the failure reason instead of silently dropping the feedback
- do not over-triage; if the user just wants a quick issue draft, keep the draft concise
- do not reopen or comment on an existing issue unless the user explicitly confirms that action

## Output Contract

For draft mode, prefer this shape:

- `Feedback type`
- `Suggested title`
- `Affected skills`
- `Issue draft`
- optional `Likely duplicates`
- optional `Recommended issue action`
- `Next action`

For confirmed external actions, prefer this shape:

- `Feedback type`
- `Issue action`
- `Issue URL`
- optional `Likely duplicates`

Use the user's primary working language when it is clear from the conversation.
Keep GitHub command names, labels, URLs, and machine-facing literals unchanged.
Surface `Skill route` and `Route reason` in the first visible update when `wilco-feedback` is selected.

## References

- Use [references/help-template.md](references/help-template.md) for `wilco-feedback help`.
- Use [references/issue-template.md](references/issue-template.md) for the issue draft shape.
