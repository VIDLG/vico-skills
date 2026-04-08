# Recommended Layout

Use one stable split between Wilco planning docs and long-lived project truth:

```text
 .wilco/
├── prd/
│   ├── active/
│   └── archive/
├── plans/
│   ├── active/
│   └── archive/
├── resume/
└── index/
docs/
├── architecture/
└── adr/
```

## Intent By Directory

- `.wilco/prd/active/`: active problem statements, scope, goals, and acceptance criteria.
- `.wilco/plans/active/`: active implementation plans and checklists.
- `.wilco/prd/archive/`: archived Wilco PRDs.
- `.wilco/plans/archive/`: archived Wilco plans.
- `.wilco/resume/`: current-only resume snapshots.
- `.wilco/index/`: machine-readable linkage manifests.
- `docs/architecture/`: current stable design truth.
- `docs/adr/`: durable architectural decisions.

## Naming Rules

- Use one topic slug across related documents.
- Prefer `kebab-case` file names.
- Keep topic names stable across lifecycle stages.

Example:

```text
.wilco/prd/active/action-pipeline.md
.wilco/plans/active/action-pipeline.md
.wilco/resume/action-pipeline.md
.wilco/index/action-pipeline.json
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
