# Wilco Routing

Use this reference when deciding what artifact set, lifecycle action, or recovery route applies.

## Entry Questions

1. Does this work already hit an existing active slug?
2. Does this work need tracked planning at all?

Treat those as separate decisions. A tiny code change can still require Wilco sync work when it advances an already-tracked slug.
`wilco-plan` is the only default front door.

## Document Levels

- `no-doc`: independent tiny work with no durable tracking value and no active slug hit
- `plan_only`: default tracked mode; one active plan carries both intent and execution
- `prd_backed`: upgraded tracked mode; an active PRD plus active plan are both maintained
- `prd + plan + architecture`: work that also creates durable system truth that belongs in `docs/architecture/`

## Lifecycle Actions

- `create`: establish a new slug and its initial artifact set
- `advance`: continue an existing tracked slug
- `reconcile`: inspect docs against code and tests after interruption or uncertainty
- `diverge-replan`: update docs because implementation reality no longer matches the current plan closely enough
- `upgrade-to-prd-backed`: add a PRD to an existing `plan_only` slug when scope framing outgrows the plan alone
- `close-cleanup`: mark the work complete, delete active planning docs, and extract durable truth into architecture docs first

## Slug Rules

- Prefer dated slugs in `YYYY-MM-DD-topic` form for new tracked work.
- Treat deleted historical docs as git history by default; do not let old work constrain new planning unless historical context is explicitly needed.
- If active overlap is small and the execution contract is still the same, reuse the current active slug.
- If active overlap is partial, ambiguous, or expensive to reconcile, delete the active docs and create one fresh dated slug instead of preserving a confusing lineage.
- Keep only one active slug per concrete execution contract whenever possible.
- When index linkage records slug relationships, use a limited vocabulary:
  - `related`
  - `follow_up`
  - `supersedes`
  - `superseded_by`

## Sync Rules

When work does not hit an active slug:

- `no-doc`: do not create or touch `.wilco/`
- tracked work should enter through `wilco-plan`
- `plan_only`: create `.wilco/plans/active/<slug>.md` and `.wilco/index/<slug>.json`
- `prd_backed`: create PRD, plan, and an index with the same slug
- `prd + plan + architecture`: create PRD, plan, index, and the architecture doc set

When work does hit an active slug:

- Do not treat the work as `no-doc` unless you explicitly choose to delete and rebuild the active docs
- Update `.wilco/index/<slug>.json` only enough to keep linkage current
- Update the PRD when scope or acceptance moved
- If a `plan_only` slug outgrows the plan alone, perform `upgrade-to-prd-backed` and mark both active docs plus index metadata accordingly
- Do not downgrade `prd_backed` to `plan_only` in place
- If overlap handling becomes more complex than a clean rewrite, prefer delete-and-rebuild over preserving the old active docs
- Update architecture docs when durable truth moved
- Update temporary reconcile state only when handing off, recovering, reconciling uncertainty, or checking closure
- Use `close-cleanup` when implementation is complete and docs need completion handling

## Out-Of-Sync Routing

When `.wilco` artifacts are outdated or disagree with code, start with `wilco-plan`.

- stale execution state: `wilco-plan`
- changed scope or acceptance: `wilco-plan`
- `plan_only` slug now needs durable scope framing: `wilco-plan` for `upgrade-to-prd-backed`
- stale architecture truth: `wilco-plan` with internal truth extraction
- effectively complete work still marked active: `wilco-plan done`
- implementation done and the user expects end-to-end completion: `wilco-exec` then `wilco-plan done`
