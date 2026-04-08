# Wilco Decision Tree

Use this reference when deciding what artifact set or lifecycle action applies.

## Entry Questions

1. Does this work already hit an existing active slug?
2. Does this work need a new artifact at all?

Treat those as separate decisions. A tiny code change can still require Wilco sync work when it advances an already-tracked slug.

## Document Levels

- `no-doc`: independent tiny work with no durable tracking value and no active slug hit
- `plan-only`: small but trackable implementation work
- `prd + plan`: medium work where goals, scope, or acceptance need durable explanation
- `prd + plan + architecture`: work that also creates durable system truth that belongs in `docs/architecture/`

## Lifecycle Actions

- `create`: establish a new slug and its initial artifact set
- `advance`: continue an existing tracked slug
- `resume`: reconcile docs against code and tests after interruption or uncertainty
- `diverge-replan`: update docs because implementation reality no longer matches the current plan closely enough
- `downgrade-to-plan-only`: retire an active PRD when it no longer provides independent scope, intent, or acceptance value
- `close-archive`: mark the work complete, archive planning docs when appropriate, and extract durable truth into architecture docs first

## Slug Rules

- Treat the slug as a stable topic ID once tracked work begins.
- Do not rename a tracked slug just because wording changed.
- If a request introduces a clearly new topic, create a new slug instead of fattening the old one.
- When splitting work into a new slug, keep the old slug focused on its original topic and record the split in both prose and index linkage.
- When index linkage records slug relationships, use a limited vocabulary:
  - `related`
  - `follow_up`
  - `supersedes`
  - `superseded_by`

## Minimal Document Strategy

- Tiny independent work with no active slug: `no-doc`
- Small work: `plan-only`
- Medium work: `prd + plan` only when scope or intent really need durable explanation
- Large or durable architecture work: `prd + plan + architecture`

Do not create a PRD for a task whose plan already captures the needed context.

## Sync Rules

When work does not hit an active slug:

- `no-doc`: do not create or touch `.wilco/`
- tracked work should enter through `wilco-init`
- `plan-only`: create `.wilco/plans/active/<slug>.md` and `.wilco/index/<slug>.json`
- `prd + plan`: create PRD, plan, and an index with the same slug
- `prd + plan + architecture`: create PRD, plan, index, and the architecture doc set

When work does hit an active slug:

- Do not treat the work as `no-doc`; always update the plan status/checklist
- Update `.wilco/index/<slug>.json` only enough to keep linkage current
- Update the PRD when scope or acceptance moved
- If a PRD no longer provides distinct value beyond the plan, perform `downgrade-to-plan-only` instead of leaving stale PRD overhead in place
- Update architecture docs when durable truth moved
- Update resume only when handing off, recovering, reconciling uncertainty, or checking closure
- Use `close-archive` when implementation is complete and docs need completion handling

## Out-Of-Sync Routing

When `.wilco` artifacts are outdated or disagree with code, start with `wilco-resume`.

- stale execution state: `wilco-resume` then `wilco-plan`
- changed scope or acceptance: `wilco-resume` then `wilco-prd` and `wilco-plan`
- active PRD no longer adds independent scope, intent, or acceptance value: `wilco-resume` then `wilco-prd` and `wilco-plan` for `downgrade-to-plan-only`
- stale architecture truth: `wilco-resume` then `wilco-docs`
- effectively complete work still marked active: `wilco-resume` then `wilco-cleanup` and `close-archive`
- implementation done and the user expects end-to-end completion: `wilco-execute` then `wilco-cleanup`
