# Recommended Layout

Use one stable top-level structure for engineering docs:

```text
docs/
├── prd/
│   ├── active/
│   └── archive/
├── plans/
│   ├── active/
│   └── archive/
├── architecture/
└── adr/
```

## Intent By Directory

- `docs/prd/active/`: active problem statements, scope, goals, and acceptance criteria.
- `docs/plans/active/`: active implementation plans and checklists.
- `docs/architecture/`: current stable design truth.
- `docs/adr/`: durable architectural decisions.
- `docs/*/archive/`: historical documents preserved for traceability.

## Naming Rules

- Use one topic slug across related documents.
- Prefer `kebab-case` file names.
- Keep topic names stable across lifecycle stages.

Example:

```text
docs/prd/active/action-pipeline.md
docs/plans/active/action-pipeline.md
docs/architecture/action-pipeline.md
```

## Lifecycle Rules

1. Start with a PRD when the work needs problem framing or scope definition.
2. Add a plan when implementation work is real and needs sequencing or checklists.
3. Extract stable facts into architecture docs once the shape is implemented or settled.
4. Archive PRD and plan documents once they stop being active sources of truth.

## Current Truth Rule

- `PRD` explains intent.
- `Plan` explains execution.
- `Architecture` explains the current system.

If contributors will need a fact six months from now, it belongs in `architecture`, not only in a completed plan.
