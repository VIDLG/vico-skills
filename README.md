# wilco-skills

Repository-native Wilco skills for planning and execution under `.wilco/`.

Chinese version: [README-zh.md](README-zh.md)
Contract map: [CONTRACTS.md](CONTRACTS.md)

## Skill Set

- `wilco-plan`: the only default front door; decide `no-doc / plan_only / prd_backed`, reconcile state, create or update the active plan, and absorb probe handoff
- `wilco-exec`: execute the active plan until complete or truly blocked
- `wilco-probe`: inspect a plan, design, or codebase; scan for issues; grill where needed; and emit a handoff block that `wilco-plan` can consume
- `wilco-feedback`: turn feedback about `wilco-skills` into a GitHub issue draft and optionally file it after explicit confirmation

For `wilco-probe` output examples, see [wilco-probe/references/output-format.md](wilco-probe/references/output-format.md).

## Default Model

- `wilco-skills` is a strongly routed workflow, not a loose toolbelt
- `wilco-plan` is the only default user-facing entrypoint
- `wilco-plan` internally handles bootstrap, lightweight reconcile, PRD escalation, and active-slug replacement decisions
- `wilco-plan` also exposes explicit controller modes such as `help`, `review`, `sync`, `prd`, `replace`, `close`, and `cancel`
- `plan_only` is the default tracked workflow
- `PRD` is an internal escalation path, not a separate default entrypoint
- once upgraded to `prd_backed`, a slug does not downgrade in place
- temporary reconcile state may still exist, but `resume` is an internal capability rather than a primary user-facing skill
- every tracked slug should have an `.wilco/index/<slug>.json` linkage file
- `index` is derived linkage metadata, not the primary human source of truth

## Design Principle

`Default Light, Escalate When Needed.`

- `wilco-skills` is designed to stay vibe-friendly at low complexity and become more structured only when the work actually needs it
- probing and execution are separate escalation axes rather than one forced heavyweight workflow
- probing can scale from direct clarification to `wilco-probe`, `scan`, and `grill`
- execution can scale from direct vibe execution to `wilco-plan`, `prd_backed`, and `wilco-exec`
- heavier modes exist to reduce ambiguity and coordination cost, not to front-load process onto every task
- workflow re-entry is first-class: work may move from vibe execution into tracked workflow and back again without being treated as an error state
- direct execution may happen before, during, or after tracked workflow; when tracked workflow resumes, the active Wilco route should reconcile against repository reality before trusting `.wilco` state

See [CONTRACTS.md](CONTRACTS.md) for the owner map, derived forms, sync policy, distribution assumptions, and validator responsibilities.

## Persistence Policy

- `wilco-probe`: keep probe state session-local by default; write back only when the user explicitly asks to capture conclusions
- `wilco-plan`: write or update active plan, optional PRD, and derived index state by default when tracked work is being shaped
- `wilco-exec`: persist plan, index, or temporary reconcile updates when continuity depends on accurate execution state or when the user expects docs to stay current

## Most Common Paths

- direct vibe execution: talk through the task and implement immediately when no tracked workflow is needed
- inspect before planning: `wilco-probe -> wilco-plan`
- refine an existing plan: `wilco-probe grill plan -> wilco-plan`
- tracked planning only: `wilco-plan`
- end-to-end tracked execution: `wilco-plan -> wilco-exec -> wilco-plan close`

## Escalation Hints

- stay in direct vibe execution when the task is local, low-risk, and does not need tracked cross-turn coordination
- use `wilco-probe` when the object is unclear, contested, or likely to benefit from evidence-first questioning before planning
- use `wilco-plan` when the work should become a tracked execution contract under `.wilco/`
- use `wilco-exec` only when an active plan already exists and the user wants persistent execution until complete or a real blocker
- if tracked work shrinks back into a local, low-risk change, prefer de-escalating back to `direct_execute`

## Route Shifts

- `direct_execute -> wilco-plan`: when local execution grows into tracked work, `wilco-plan` should perform the minimum reconcile or sync needed to re-anchor on current repository reality
- `wilco-plan -> direct_execute`: when the remaining work is small and low-risk, prefer a lighter route instead of keeping the user inside a heavier Wilco path
- `wilco-probe -> direct_execute`: when probe concludes that the next safe action is local implementation, route directly instead of forcing planning
- if tracked work shrinks back into a local, low-risk change, prefer de-escalating back to `direct_execute`

## Route Shifts

- `direct_execute -> wilco-plan`: when local execution grows into tracked work, `wilco-plan` should perform the minimum reconcile or sync needed to re-anchor on current repository reality
- `wilco-plan -> direct_execute`: when the remaining work is small and low-risk, prefer a lighter route instead of keeping the user inside a heavier Wilco path
- `wilco-probe -> direct_execute`: when probe concludes that the next safe action is local implementation, route directly instead of forcing planning

## Natural Triggers

- `wilco-probe`: `scan the repo`, `inspect the codebase`, `grill this plan`, `refine this plan`, `how do I use wilco-probe`
- `wilco-plan`: `make a plan`, `create a tracked plan`, `turn this into execution steps`, `reconcile the current plan`, `verify this plan`, `verify close`, `verify sync`, `verify replan`, `how do I use wilco-plan`
- `wilco-exec`: `keep going`, `continue until complete`, `execute the active plan`, `carry this through unless blocked`, `how do I use wilco-exec`
- `wilco-feedback`: `file an issue`, `report a bug`, `I have feedback about wilco-skills`, `draft a GitHub issue`, `how do I use wilco-feedback`

If a natural-language request could reasonably mean more than one of these routes, prefer a short clarification over guessing the wrong workflow.

## Route Visibility

- When a Wilco skill is selected, the first visible update should surface the active skill and the route reason.
- Suggested shape:
  - `Skill route: <skill-name>`
  - `Route reason: <natural trigger | explicit skill request>`
- For explicit skill invocations, surface that the route came from an explicit skill request rather than a natural trigger.

## When To Use What

- Need to start, update, reconcile, or reshape tracked work: `wilco-plan`
- Need to verify that a plan is really complete against the current codebase before close-out: `wilco-plan verify`
- Continue implementation against an active plan: `wilco-exec`
- Need to close out or cancel tracked work and remove active docs: `wilco-plan`
- Need architecture truth extraction or boundary handling: `wilco-plan`
- Need to inspect a plan, design, or codebase before planning: `wilco-probe`
- Need to turn feedback into a GitHub issue draft or file it after confirmation: `wilco-feedback`

`wilco-feedback` should auto-classify the report as `bug`, `ux_friction`, `contract_gap`, or `feature_request` unless the category is genuinely ambiguous.
When likely duplicates exist, `wilco-feedback` should prefer a draft recommendation of `create`, `reopen`, or `comment` rather than always assuming a new issue.

## Feedback Flow

If you hit a bug, confusing workflow, naming problem, or feature gap in `wilco-skills`, use `wilco-feedback`.

Typical flow:

1. Describe the problem in natural language.
2. Let `wilco-feedback` classify it and draft the issue.
3. Review the suggested draft and duplicate handling recommendation.
4. Say `create it`, `reopen it`, or `comment there` only if you want the external GitHub action to happen.

Example prompts:

- `I have feedback about wilco-skills`
- `this workflow feels awkward`
- `report a bug in wilco-plan`
- `draft a GitHub issue for this`

## Automation

- `wilco-plan/scripts/bootstrap_wilco_slug.py`
  Creates starter active plan/PRD/architecture files when `wilco-plan` decides a new slug is needed.
- `wilco-plan/scripts/sync_wilco_headers.py`
  Synchronizes plan and PRD headers plus cross-links.
- `wilco-plan/scripts/sync_wilco_index.py`
  Rebuilds minimal `.wilco/index/*.json` manifests from current artifacts.
- `wilco-plan/scripts/close_wilco_slug.py`
  Deletes completed active docs and clears temporary resume/index state.
- `wilco-plan/scripts/validate_wilco_workspace.py`
  Validates the current `.wilco` workspace against the Wilco schema.
- `scripts/validate_wilco_skills.py`
  Validates all Wilco skills, helper scripts, tests, and basic content hygiene.

## Install And Uninstall

Recommended install path: use `npx skills@latest`.

### Install With `npx skills@latest`

Install one skill for a specific agent:

```bash
npx skills@latest add VIDLG/wilco-skills --skill wilco-probe --agent codex
npx skills@latest add VIDLG/wilco-skills --skill wilco-plan --agent codex
npx skills@latest add VIDLG/wilco-skills --skill wilco-exec --agent codex
```

Install all Wilco skills for all supported agents:

```bash
npx skills@latest add VIDLG/wilco-skills --all
```

List available skills without installing:

```bash
npx skills@latest add VIDLG/wilco-skills --list
```

The `skills` CLI can also take a GitHub URL directly.
For Claude Code, use the same commands with `--agent claude-code`.

Reference:

- Vercel Skills docs: https://vercel.com/docs/agent-resources/skills
- Vercel skills guide: https://vercel.com/kb/guide/agent-skills-creating-installing-and-sharing-reusable-agent-context

### Uninstall With `npx skills@latest`

Remove one skill:

```bash
npx skills@latest remove wilco-probe
npx skills@latest remove wilco-plan
npx skills@latest remove wilco-exec
```

### Development Link

For local development, link the skill directories into your agent's skills folder instead of copying them.

- Codex: link into `.codex/skills/`
- Claude Code: link into `.claude/skills/`
- Unix-like systems: use `ln -s`
- Windows: use symbolic links or junctions

### Uninstall

Remove the installed skill directories or delete the development links from your agent's skills folder.

## Typical Flows

### Start Or Reconcile Work

```text
wilco-plan
```

### Inspect Current State

```text
wilco-plan review
```

### Verify Before Close-Out

```text
wilco-plan verify
```

`verify` should recommend both:

- a human-facing `Recommended action`
- an internal `Recommended Next Mode`

### Verify Then Close Out

```text
wilco-plan verify close
```

### Verify Then Sync

```text
wilco-plan verify sync
```

### Verify Then Replan

```text
wilco-plan verify replan
```

### Show Available Modes

```text
wilco-plan help
```

### Probe Then Plan

```text
wilco-probe -> wilco-plan
```

### Show Available Modes

```text
wilco-exec help
wilco-probe help
```

## Probe Workflow

- `wilco-probe`
  - default entry; does a light scan first, then recommends, asks one question, reviews, or resolves based on issue state
- `wilco-probe scan`
  - deep inspection only; build evidence, issues, and a topic map without entering a long questioning loop
- `wilco-probe grill`
  - force sustained high-intensity questioning on the most important unresolved issues
- `wilco-probe grill plan`
  - grill the current active plan as the target object and refine plan text when low-risk clarifications can be applied immediately
- `wilco-probe review`
  - show the current accepted decisions, unresolved issues, and suggested next mode
- `wilco-probe resolve`
  - stop asking and emit a final summary or `Probe Handoff` for `wilco-plan`
- `wilco-probe help`
  - show the modes and the intended usage flow

### Execute And Finish

```text
wilco-exec -> wilco-plan close
```

The lifecycle remains simple even when the user wants end-to-end completion:

- `wilco-exec` finishes implementation and keeps the plan current
- `wilco-plan close` performs close-out deletion handling
- agents may route automatically from `wilco-exec` into `wilco-plan close` so the user does not need to remember the second step

## Development Notes

- Treat `wilco-skills/` as the single source of truth.
- During development, point project-local `.codex/skills/` and `.claude/skills/` entries at these folders instead of copying skill contents.
- For Claude Code, hook scripts live in `wilco-exec/scripts/` and project hook wiring lives in `.claude/settings*.json`.

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
