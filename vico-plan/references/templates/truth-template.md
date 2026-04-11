# Truth Template

Use this shape for `vico-plan truth`.
Render headings and prose in the user's primary working language when it is clear from the conversation.
Keep commands, path literals, and stable field labels unchanged when another workflow consumes them.

```md
## Truth Extraction

- Source slug: ...
- Target doc: `docs/architecture/...`
- Reason: why this belongs in long-lived truth

## Stable Facts

- ...
- ...

## Excluded From Truth

- execution-only details that remain in the active plan
- temporary migration or checklist state
```

Use `truth` only when the user explicitly asks for durable truth extraction.
