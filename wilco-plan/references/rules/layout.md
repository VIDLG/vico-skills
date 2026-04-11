# Recommended Layout

Use one stable split between Wilco planning docs and long-lived project truth:

```text
 .wilco/
├── prd/
│   └── active/
├── plans/
│   └── active/
├── resume/
└── index/
docs/
├── architecture/
└── adr/
```

## Intent By Directory

- `.wilco/plans/active/`: default active documents. In `plan_only`, each plan carries both problem framing and execution. In `prd_backed`, plans focus on execution and link to the PRD.
- `.wilco/prd/active/`: active PRDs for `prd_backed` slugs only.
- `.wilco/resume/`: current-only handoff or reconciliation snapshots created on demand.
- `.wilco/index/`: minimal machine-readable linkage manifests that can be rebuilt.
- `docs/architecture/`: current stable design truth.
- `docs/adr/`: durable architectural decisions.

## Naming Rules

- Prefer `YYYY-MM-DD-topic` slugs for new tracked work.
- Use one slug across related active documents for the same execution contract.
- Prefer `kebab-case` file names.
- Deleted historical docs live in git history and do not need to constrain future naming.

Example:

```text
.wilco/prd/active/2026-04-09-action-pipeline.md
.wilco/plans/active/2026-04-09-action-pipeline.md
.wilco/resume/2026-04-09-action-pipeline.md
.wilco/index/2026-04-09-action-pipeline.json
docs/architecture/2026-04-09-action-pipeline.md
```

## Lifecycle Rules

1. Start with `no-doc` or `plan_only` unless the work clearly needs more structure.
2. Add a PRD only when the work needs problem framing, durable scope, or user-facing acceptance beyond the plan.
3. When upgrading to `prd_backed`, mark the plan, PRD, and index linkage explicitly.
4. Do not downgrade `prd_backed` back to `plan_only` in place; close and restart if simplification is truly needed.
5. If active overlap becomes confusing, prefer delete-and-rebuild with one fresh dated slug.
6. Create resume snapshots only when recovering, handing off, reconciling divergence, or checking completion.
7. Keep the index minimal; treat it as derived linkage, not as an equal source of human truth.
8. Extract stable facts into architecture docs once the shape is implemented or settled.
9. Delete PRD and plan documents from `active/` once they stop being active sources of truth.

## Current Truth Rule

- `Plan` is the default active source of truth.
- In `plan_only`, the plan explains both intent and execution.
- In `prd_backed`, the PRD explains intent and the plan explains execution.
- `Architecture` explains the current system.
- `Resume` explains a temporary verified handoff state.
- `Index` only links the current artifact set.

If contributors will need a fact six months from now, it belongs in `architecture`, not only in a completed plan.
