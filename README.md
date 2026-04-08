# wilco-skills

Repository-native Wilco skills for planning, execution, reconciliation, and cleanup under `.wilco/`.

Chinese version: [README-zh.md](README-zh.md)
Contract map: [CONTRACTS.md](CONTRACTS.md)

## Skill Set

- `wilco-init`: bootstrap a new slug with the smallest valid artifact set
- `wilco-plan`: default tracked workflow; create or update plan-only or PRD-backed execution plans
- `wilco-prd`: create or update PRDs only when plan-only is not enough
- `wilco-resume`: reconcile `.wilco`, code, and tests to decide the true current state
- `wilco-execute`: execute the active plan until done or truly blocked
- `wilco-cleanup`: archive completed or abandoned slugs and clear stale temporary state
- `wilco-docs`: govern `.wilco` vs `docs/` boundaries, lifecycle, and archive handling
- `wilco-grill`: stress-test the current PRD, plan, or design

For `wilco-grill` output examples, see [wilco-grill/references/output-format.md](wilco-grill/references/output-format.md).

## Default Model

- `wilco-skills` is a strongly routed workflow, not a loose toolbelt
- new tracked work enters through `wilco-init`
- `plan-only` is the default tracked workflow
- `PRD` is an escalation, not a baseline requirement
- `resume` is a temporary handoff or recovery snapshot
- every tracked slug should have an `.wilco/index/<slug>.json` linkage file
- `index` is derived linkage metadata, not the primary human source of truth

See [CONTRACTS.md](CONTRACTS.md) for the owner map, derived forms, sync policy, distribution assumptions, and validator responsibilities.

## When To Use What

- New tracked work, no slug yet: `wilco-init`
- Existing slug, need execution planning: `wilco-plan`
- Existing slug, scope or acceptance changed: `wilco-prd` and `wilco-plan`
- `.wilco` looks outdated or out of sync: `wilco-resume`
- Continue implementation against an active plan: `wilco-execute`
- Work is effectively done and should be archived: `wilco-cleanup`
- Need lifecycle or placement decisions: `wilco-docs`

Do not bootstrap new tracked work from `wilco-plan` or `wilco-prd`. Those skills may update an existing slug directly, but new tracked work should first enter the workflow through `wilco-init`.

## Automation

- `wilco-init/scripts/bootstrap_wilco_slug.py`
  Creates starter plan/PRD/architecture files for a new slug.
- `wilco-docs/scripts/sync_wilco_headers.py`
  Synchronizes plan and PRD headers plus cross-links.
- `wilco-docs/scripts/sync_wilco_index.py`
  Rebuilds minimal `.wilco/index/*.json` manifests from current artifacts.
- `wilco-docs/scripts/close_wilco_slug.py`
  Archives a completed slug and clears temporary resume/index state.
- `wilco-docs/scripts/validate_wilco_workspace.py`
  Validates the current `.wilco` workspace against the Wilco schema.
- `scripts/validate_wilco_skills.py`
  Validates all Wilco skills, helper scripts, tests, and basic content hygiene.

## Typical Flows

### Start New Work

```text
wilco-init -> wilco-plan
```

or:

```text
wilco-init -> wilco-prd -> wilco-plan
```

### Recover Out-Of-Sync Work

```text
wilco-resume -> wilco-plan
wilco-resume -> wilco-prd -> wilco-plan
wilco-resume -> wilco-docs
```

### Execute And Close

```text
wilco-execute -> wilco-cleanup
```

The skill boundary remains split even when the user wants end-to-end completion:

- `wilco-execute` finishes implementation and keeps the plan current
- `wilco-cleanup` performs `close-archive` handling
- agents may route automatically from `wilco-execute` into `wilco-cleanup` so the user does not need to remember the second step

## Development Notes

- Treat `wilco-skills/` as the single source of truth.
- During development, point project-local `.codex/skills/` and `.claude/skills/` entries at these folders instead of copying skill contents.
- For Claude Code, hook scripts live in `wilco-execute/scripts/` and project hook wiring lives in `.claude/settings*.json`.

## Validation

Run:

```text
python3 wilco-skills/scripts/validate_wilco_skills.py
```

This runs:

- `quick_validate` on every Wilco skill
- `py_compile` on helper scripts
- fixture-based automation tests
- lightweight workflow invariant checks
- placeholder and `__pycache__` hygiene checks
