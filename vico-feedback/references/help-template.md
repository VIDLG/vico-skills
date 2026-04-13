# Help Template

Use this shape for `vico-feedback help`.
Render headings and prose in the user's primary working language when it is clear from the conversation.
Keep commands, labels, and GitHub literals unchanged.

```md
## Vico Feedback Help

- Entry: `vico-feedback`
- Default role: turn feedback about `vico-skills` into a GitHub issue draft

## Behavior

- classify feedback as bug, UX friction, contract gap, or feature request
- classify the feedback automatically from the user's wording unless the category is genuinely ambiguous
- draft an issue before creating anything
- check likely duplicates when useful
- suggest `create`, `reopen`, or `comment` when a duplicate check finds a likely existing issue
- create the GitHub issue only after explicit user confirmation
- show this route-debug shape in the first visible update:
  - `Skill route: vico-feedback`
  - `Route reason: <explicit_skill_request | intent_cluster | natural_trigger>`
  - optional `Route detail: <workflow_feedback | issue_draft_request | exact trigger phrase>`
  - optional `Route mode: <default | help>`

## Outputs

- `Feedback type`
- `Suggested title`
- `Affected skills`
- `Issue draft`
- `Recommended issue action`
- `Next action`

## Examples

- `I have feedback about vico-skills`
- `提个 issue`
- `这个触发不太对`
- `draft an issue for this`
- `file a bug against vico-plan`
- `how do I use vico-feedback`
```

Keep help compact and action-oriented.
