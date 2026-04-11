# Help Template

Use this shape for `wilco-feedback help`.
Render headings and prose in the user's primary working language when it is clear from the conversation.
Keep commands, labels, and GitHub literals unchanged.

```md
## Wilco Feedback Help

- Entry: `wilco-feedback`
- Default role: turn feedback about `wilco-skills` into a GitHub issue draft

## Behavior

- classify feedback as bug, UX friction, contract gap, or feature request
- classify the feedback automatically from the user's wording unless the category is genuinely ambiguous
- draft an issue before creating anything
- check likely duplicates when useful
- suggest `create`, `reopen`, or `comment` when a duplicate check finds a likely existing issue
- create the GitHub issue only after explicit user confirmation
- surface `Skill route` and `Route reason` in the first visible update

## Outputs

- `Feedback type`
- `Suggested title`
- `Affected skills`
- `Issue draft`
- `Recommended issue action`
- `Next action`

## Examples

- `I have feedback about wilco-skills`
- `draft an issue for this`
- `file a bug against wilco-plan`
- `how do I use wilco-feedback`
```

Keep help compact and action-oriented.
