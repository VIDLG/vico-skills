# vico-skills

Repository-native Vico skills for planning and execution under `.vico/`.

Chinese version: [README-zh.md](README-zh.md)
Contract map: [CONTRACTS.md](CONTRACTS.md)

## Why Vico?

`Vico` is a mutation of `Wilco`.

- it keeps the recognizable `-co` sound from `Wilco`, so the name still feels related rather than completely reset
- it drops the heavier `Wil` feel and replaces it with `Vi`, which points more toward vibe, lighter interaction, and lower-friction workflow
- the intent is the same reliable execution core, but with a friendlier surface: default light, escalate when needed, and de-escalate when complexity drops

The repo still uses `vico-*` skill names today. `vico-skills` is the broader project identity around that workflow style.

## Skill Set

- `vico-grill`: freeform sustained questioning for ideas, tradeoffs, and decisions before repository evidence matters
- `vico-plan`: the only default front door; decide `no-doc / plan_only / prd_backed`, reconcile state, create or update the active plan, and absorb probe handoff
- `vico-exec`: execute the active plan until complete or truly blocked
- `vico-probe`: inspect a plan, design, or codebase; scan for issues; grill where needed; and emit a handoff block that `vico-plan` can consume
- `vico-feedback`: turn feedback about `vico-skills` into a GitHub issue draft and optionally file it after explicit confirmation

For `vico-probe` output examples, see [vico-probe/references/output-format.md](vico-probe/references/output-format.md).

## Default Model

- `vico-skills` is a strongly routed workflow, not a loose toolbelt
- `vico-plan` is the only default user-facing entrypoint
- `vico-plan` internally handles bootstrap, lightweight reconcile, PRD escalation, and active-slug replacement decisions
- `vico-plan` also exposes explicit controller modes such as `help`, `review`, `sync`, `prd`, `replace`, `close`, and `cancel`
- `plan_only` is the default tracked workflow
- `PRD` is an internal escalation path, not a separate default entrypoint
- once upgraded to `prd_backed`, a slug does not downgrade in place
- temporary reconcile state may still exist, but `resume` is an internal capability rather than a primary user-facing skill
- every tracked slug should have an `.vico/index/<slug>.json` linkage file
- `index` is derived linkage metadata, not the primary human source of truth

## Design Principle

`Default Light, Escalate When Needed.`

- `vico-skills` is designed to stay vibe-friendly at low complexity and become more structured only when the work actually needs it
- probing and execution are separate escalation axes rather than one forced heavyweight workflow
- freeform grilling is the lightest questioning lane
- problem framing and execution structure are separate escalation axes rather than one forced heavyweight workflow
- freeform grilling is the lightest problem-framing lane; `vico-probe` is the repo-native problem-framing lane
- freeform questioning can scale from `vico-grill` into `vico-probe` or `vico-plan` when repository reality or tracked execution becomes the next governing constraint
- probing can scale from direct clarification to `vico-probe`, `scan`, and `grill`
- execution can scale from direct vibe execution to `vico-plan`, `prd_backed`, and `vico-exec`
- heavier modes exist to reduce ambiguity and coordination cost, not to front-load process onto every task
- workflow re-entry is first-class: work may move from vibe execution into tracked workflow and back again without being treated as an error state
- direct execution may happen before, during, or after tracked workflow; when tracked workflow resumes, the active Vico route should reconcile against repository reality before trusting `.vico` state

### Escalation Map

```text
Higher execution structure
^
|                                      vico-exec
|                           vico-plan (plan_only / prd_backed)
|                  vico-probe -> vico-plan
|         vico-probe
|  vico-grill
+------------------------------------------------------------> Higher problem-framing rigor
  direct vibe execution
```

- Horizontal axis: problem-framing rigor
  how much discovery, clarification, and repository-grounded reasoning is needed before action is safe
- Vertical axis: execution structure
  how much durable planning, coordination, and repeatable execution machinery the work now needs
- Move right when the problem is still unclear or contested.
- Move up when the execution needs stronger contracts, artifacts, or persistence.

See [CONTRACTS.md](CONTRACTS.md) for the owner map, derived forms, sync policy, distribution assumptions, and validator responsibilities.

## Persistence Policy

- `vico-grill`: keep freeform grill state session-local by default and do not write `.vico` artifacts
- `vico-probe`: keep probe state session-local by default; write back only when the user explicitly asks to capture conclusions
- `vico-plan`: write or update active plan, optional PRD, and derived index state by default when tracked work is being shaped
- `vico-exec`: persist plan, index, or temporary reconcile updates when continuity depends on accurate execution state or when the user expects docs to stay current

## Most Common Paths

- freeform questioning: `vico-grill`
- freeform questioning into formal inspection: `vico-grill -> vico-probe`
- freeform questioning into tracked work: `vico-grill -> vico-plan`
- direct vibe execution: talk through the task and implement immediately when no tracked workflow is needed
- inspect before planning: `vico-probe -> vico-plan`
- refine an existing plan: `vico-probe grill plan -> vico-plan`
- tracked planning only: `vico-plan`
- cross-agent handoff: `Codex vico-plan -> Claude Code vico-exec`
- Claude runner loop: `Codex vico-plan -> Claude runner -> vico-plan verify`
- end-to-end tracked execution: `vico-plan -> vico-exec -> vico-plan close`

## Escalation Hints

- use `vico-grill` when the user wants freeform sustained questioning on an idea, tradeoff, or decision before repository evidence matters
- stay in direct vibe execution when the task is local, low-risk, and does not need tracked cross-turn coordination
- use `vico-probe` when the object is unclear, contested, or likely to benefit from evidence-first questioning before planning
- use `vico-plan` when the work should become a tracked execution contract under `.vico/`
- use `vico-exec` only when an active plan already exists and the user wants persistent execution until complete or a real blocker
- if tracked work shrinks back into a local, low-risk change, prefer de-escalating back to `direct_execute`

## Route Shifts

- `vico-grill -> vico-probe`: when freeform questioning hits a repo plan, PRD, design, codebase, or any question that now depends on repository evidence
- `vico-grill -> vico-plan`: when the questioning is already sufficient to define tracked work under `.vico/`
- `direct_execute -> vico-plan`: when local execution grows into tracked work, `vico-plan` should perform the minimum reconcile or sync needed to re-anchor on current repository reality
- `vico-plan -> direct_execute`: when the remaining work is small and low-risk, prefer a lighter route instead of keeping the user inside a heavier Vico path
- `vico-probe -> direct_execute`: when probe concludes that the next safe action is local implementation, route directly instead of forcing planning
- if tracked work shrinks back into a local, low-risk change, prefer de-escalating back to `direct_execute`

## Natural Triggers

- `vico-grill`: `grill this idea`, `grill me`, `stress-test this decision`, `deep interview this`, `discuss this tradeoff`, `how do I use vico-grill`
- `vico-probe`: `scan the repo`, `inspect the codebase`, `grill this plan`, `grill this PRD`, `refine this plan`, `how do I use vico-probe`
- `vico-plan`: `make a plan`, `create a tracked plan`, `turn this into execution steps`, `reconcile the current plan`, `verify this plan`, `verify close`, `verify sync`, `verify replan`, `close this plan`, `export these rules to AGENTS.md`, `write the operating brief to CLAUDE.md`, `how do I use vico-plan`
- `vico-exec`: `keep going`, `continue until complete`, `execute the active plan`, `carry this through unless blocked`, `vico-exec cc`, `run this with cc`, `handoff to cc`, `use claude code runner`, `how do I use vico-exec`
- `vico-feedback`: `file an issue`, `report a bug`, `I have feedback about vico-skills`, `draft a GitHub issue`, `how do I use vico-feedback`

If a natural-language request could reasonably mean more than one of these routes, prefer a short clarification over guessing the wrong workflow.
If the wording is just `grill this` or `grill this problem`, prefer `vico-grill` unless the user also names a repo object.
If the wording is `grill this plan`, `grill this PRD`, or points at `.vico`, prefer `vico-probe`.

## Route Visibility

- When a Vico skill is selected, the first visible update should surface the active skill and the route reason.
- Suggested shape:
  - `Skill route: <skill-name>`
  - `Route reason: <natural trigger | explicit skill request>`
- For explicit skill invocations, surface that the route came from an explicit skill request rather than a natural trigger.

## When To Use What

- Need to pressure-test an idea, decision, or tradeoff before repository evidence matters: `vico-grill`
- Need to start, update, reconcile, or reshape tracked work: `vico-plan`
- Need to verify that a plan is really complete against the current codebase before close-out: `vico-plan verify`
- Continue implementation against an active plan: `vico-exec`
- Need to close out or cancel tracked work and remove active docs: `vico-plan`
- Need architecture truth extraction or boundary handling: `vico-plan`
- Need to inspect a plan, design, or codebase before planning: `vico-probe`
- Need to turn feedback into a GitHub issue draft or file it after confirmation: `vico-feedback`

`vico-feedback` should auto-classify the report as `bug`, `ux_friction`, `contract_gap`, or `feature_request` unless the category is genuinely ambiguous.
When likely duplicates exist, `vico-feedback` should prefer a draft recommendation of `create`, `reopen`, or `comment` rather than always assuming a new issue.

## Feedback Flow

If you hit a bug, confusing workflow, naming problem, or feature gap in `vico-skills`, use `vico-feedback`.

Typical flow:

1. Describe the problem in natural language.
2. Let `vico-feedback` classify it and draft the issue.
3. Review the suggested draft and duplicate handling recommendation.
4. Say `create it`, `reopen it`, or `comment there` only if you want the external GitHub action to happen.

Example prompts:

- `I have feedback about vico-skills`
- `this workflow feels awkward`
- `report a bug in vico-plan`
- `draft a GitHub issue for this`

## Automation

- `vico-plan/scripts/bootstrap_vico_slug.py`
  Creates starter active plan/PRD/architecture files when `vico-plan` decides a new slug is needed.
- `vico-plan/scripts/sync_vico_headers.py`
  Synchronizes plan and PRD headers plus cross-links.
- `vico-plan/scripts/sync_vico_index.py`
  Rebuilds minimal `.vico/index/*.json` manifests from current artifacts.
- `vico-plan/scripts/close_vico_slug.py`
  Deletes completed active docs and clears temporary resume/index state.
- `vico-plan/scripts/validate_vico_workspace.py`
  Validates the current `.vico` workspace against the Vico schema.
- `scripts/validate_vico_skills.py`
  Validates all Vico skills, helper scripts, tests, and basic content hygiene.

## Install And Uninstall

Recommended install path: use `npx skills@latest`.

### Install With `npx skills@latest`

Install one skill for a specific agent:

```bash
npx skills@latest add VIDLG/vico-skills --skill vico-grill --agent codex
npx skills@latest add VIDLG/vico-skills --skill vico-probe --agent codex
npx skills@latest add VIDLG/vico-skills --skill vico-plan --agent codex
npx skills@latest add VIDLG/vico-skills --skill vico-exec --agent codex
npx skills@latest add VIDLG/vico-skills --skill vico-feedback --agent codex
```

Install all Vico skills for all supported agents:

```bash
npx skills@latest add VIDLG/vico-skills --all
```

List available skills without installing:

```bash
npx skills@latest add VIDLG/vico-skills --list
```

The `skills` CLI can also take a GitHub URL directly.
For Claude Code, use the same commands with `--agent claude-code`.

Reference:

- Vercel Skills docs: https://vercel.com/docs/agent-resources/skills
- Vercel skills guide: https://vercel.com/kb/guide/agent-skills-creating-installing-and-sharing-reusable-agent-context

### Uninstall With `npx skills@latest`

Remove one skill:

```bash
npx skills@latest remove vico-grill
npx skills@latest remove vico-probe
npx skills@latest remove vico-plan
npx skills@latest remove vico-exec
npx skills@latest remove vico-feedback
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
vico-plan
```

### Inspect Current State

```text
vico-plan review
```

### Verify Before Close-Out

```text
vico-plan verify
```

`verify` should recommend both:

- a human-facing `Recommended action`
- an internal `Recommended Next Mode`

### Verify Then Close Out

```text
vico-plan verify close
```

### Verify Then Sync

```text
vico-plan verify sync
```

### Verify Then Replan

```text
vico-plan verify replan
```

### Show Available Modes

```text
vico-plan help
```

### Probe Then Plan

```text
vico-probe -> vico-plan
```

### Export Repo Operating Brief

```text
vico-plan export-md AGENTS.md
vico-plan export-md CLAUDE.md
```

Use this when you want the current Vico discipline and repo-local workflow rules exported into project-local instruction files.

### Show Available Modes

```text
vico-exec help
vico-probe help
```

## Probe Workflow

- `vico-probe`
  - default entry; does a light scan first, then recommends, asks one question, reviews, or resolves based on issue state
- `vico-probe scan`
  - deep inspection only; build evidence, issues, and a topic map without entering a long questioning loop
- `vico-probe grill`
  - force sustained high-intensity questioning on the most important unresolved issues
- `vico-probe grill plan`
  - grill the current active plan as the target object and refine plan text when low-risk clarifications can be applied immediately
- `vico-probe review`
  - show the current accepted decisions, unresolved issues, and suggested next mode
- `vico-probe resolve`
  - stop asking and emit a final summary or `Probe Handoff` for `vico-plan`
- `vico-probe help`
  - show the modes and the intended usage flow

### Execute Then Manually Close

```text
vico-exec -> user confirms -> vico-plan close
```

The lifecycle remains simple even when the user wants end-to-end completion:

- `vico-exec` finishes implementation and keeps the plan current
- `vico-plan close` performs close-out deletion handling
- agents should stop after showing completion evidence and wait for the user to type the close command explicitly

### Codex Plan Then Claude Execute

```text
Codex: vico-plan -> Claude Code: vico-exec
```

This is a first-class supported handoff:

- Codex can build or refine the tracked plan
- Claude Code can consume the active plan and execute it
- handoff happens through the active `.vico` artifacts rather than hidden session state

### Claude Runner Loop

```bash
python3 vico-skills/vico-exec/scripts/claude_exec_runner.py --repo-root D:/projects/spoon
```

Use the runner when Claude Code should keep looping through execute + verify + continue decisions until it reaches `done`, `blocked`, `needs_user`, or `stale_plan`.
Natural entrypoints: `vico-exec cc`, `run this with cc`, `handoff to cc`.

## External Influences

These references influenced the shape of `vico-skills`, even though Vico keeps its own contracts and naming:

- [`forrestchang/andrej-karpathy-skills`](https://github.com/forrestchang/andrej-karpathy-skills)
  influenced the emphasis on explicit assumptions, simplicity pressure, surgical changes, and goal-driven execution. Those ideas map closely onto Vico's evidence-first probing, small-scope edits, and verify-driven execution loops.
- [`mattpocock/skills` `grill-me`](https://github.com/mattpocock/skills/tree/main/grill-me)
  influenced the freeform grilling lane behind `vico-grill`, especially the one-question-at-a-time pressure-testing style.
- [`gsd-build/get-shit-done`](https://github.com/gsd-build/get-shit-done)
  influenced the emphasis on repo-local planning artifacts and context-engineered execution. GSD currently keeps planning state under `.plans/`.
- [`Yeachan-Heo/oh-my-codex`](https://github.com/Yeachan-Heo/oh-my-codex)
  influenced the idea of a workflow layer around Codex, durable runtime state under `.omx/`, and persistent completion loops such as `$ralph`.
- [`Yeachan-Heo/oh-my-claudecode`](https://github.com/Yeachan-Heo/oh-my-claudecode)
  influenced the Claude Code side of the model: team orchestration, staged execution pipelines, and explicit Codex/Claude cross-runtime handoff surfaces.

Vico intentionally stays smaller and more repo-native than those systems. These are inspirations, not compatibility targets.

## Development Notes

- Treat `vico-skills/` as the single source of truth.
- During development, point project-local `.codex/skills/` and `.claude/skills/` entries at these folders instead of copying skill contents.
- For Claude Code, hook scripts live in `vico-exec/scripts/` and project hook wiring lives in `.claude/settings*.json`.
- For Claude Code, the stronger outer-loop runner lives at `vico-exec/scripts/claude_exec_runner.py`.

## Validation

Run:

```text
python3 vico-skills/scripts/validate_vico_skills.py
```

This runs:

- `quick_validate` on every Vico skill
- `py_compile` on helper scripts
- fixture-based automation tests
- lightweight workflow invariant checks
- placeholder and `__pycache__` hygiene checks
