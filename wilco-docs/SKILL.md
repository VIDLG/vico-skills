---
name: wilco-docs
description: Repository documentation governance for Wilco-style engineering docs. Use when organizing or evolving repo-local planning docs under `.wilco/`, long-lived architecture docs under `docs/`, deciding where docs belong, defining document lifecycle rules, choosing the minimal document set for a task, archiving completed plans or PRDs, or separating current architecture truth from historical planning records.
---

# Docs Governance

## Overview

Treat engineering documentation as a lifecycle with two distinct layers:

- `.wilco/` for Wilco planning and execution docs
- `docs/` for long-lived project truth

Keep planning docs, active PRDs, and active plans under `.wilco/`. Keep durable architecture truth and decision records under `docs/`. Make document status explicit whenever a document stops being active.

`.wilco/` is an opt-in workspace. A repository does not need it at birth. Create it when the project starts using Wilco planning, resume, or execution workflows.

Do not maximize document count. Prefer the smallest document set that is sufficient for the task.

## Minimal Defaults

Default to the smallest artifact set that keeps the work clear:

- new tracked work enters through `wilco-init`
- `plan-only` is the default tracked workflow
- `PRD` is an escalation for work that needs durable scope framing
- `resume` is on-demand, not mandatory per slug
- `index` exists for tracked slugs as a lightweight derived coordination file, not a primary human document

Do not create all artifacts just because Wilco exists in the repository.

## Quick Start

1. Inspect the current `docs/` tree and identify mixed responsibilities, duplicate topics, and historical documents posing as current truth.
2. Use [references/decision-tree.md](references/decision-tree.md) to choose the document level and lifecycle action.
3. Make the smallest structural or lifecycle change that clarifies ownership and status.
4. Cross-link replacement documents whenever archiving or superseding older ones.

## Classification Rules

- `PRD`: why the change exists, goals, non-goals, scope, acceptance criteria. In Wilco flows, these normally live under `.wilco/prd/`.
- `Plan`: how to implement the change, phases, migration steps, validation, checklist. In Wilco flows, these normally live under `.wilco/plans/`.
- `Architecture`: the current stable design that future contributors should treat as truth. These should live under `docs/architecture/`.
- `ADR`: a durable architectural decision with context, alternatives, and consequences.
- `Archive`: historical material that is intentionally preserved but no longer drives current work.

Never let `.wilco` planning docs stand in for long-lived architecture truth. If a completed PRD or plan still contains facts contributors will need later, extract those facts into `docs/architecture/` before or alongside archival work.

## Boundary Rules

- `.wilco/` is for active planning, execution tracking, and planning-history artifacts.
- `docs/architecture/` is for current stable truth that should outlive any one plan.
- `docs/adr/` is for key decisions and their rationale, not for current full-system descriptions.
- Do not move planning churn into `docs/architecture/`.
- Do not leave durable truth trapped only in `.wilco/`.

## Working Rules

- Prefer one topic slug across related docs: the same subject should map cleanly across PRD, plan, and architecture files.
- Treat the slug as a stable topic identifier once work is tracked. If a clearly new topic emerges, create a follow-up slug instead of renaming the old one.
- Prefer explicit status over silent historical drift: add `Status`, completion date, and replacement links when archiving.
- Prefer explicit document dates in the header: use stable file names and put `Created`, `Updated`, `Completed`, or review dates in document metadata instead of encoding dates into file names.
- Prefer directory clarity over root-level sprawl: active docs should be easy to distinguish from historical docs at a glance.
- Prefer migration by extraction, not by deletion: move stable truth into architecture docs before retiring planning documents.
- Prefer minimal churn: do not rename or relocate unrelated docs in the same change.
- If work hits an existing active slug, prefer updating the existing artifact set over creating a new sibling slug.
- If work hits an existing active slug, do not treat the change as `no-doc`; update the tracked artifact set at least at the plan layer.
- If tracked work changes only implementation progress, update the plan and derived linkage before considering PRD or architecture changes.
- If tracked work changes goals, scope, non-goals, or acceptance criteria, update the PRD as well.
- If an active PRD no longer adds independent value beyond the plan, perform `downgrade-to-plan-only` explicitly instead of leaving the PRD active forever.
- If tracked work creates durable design truth, update `docs/architecture/` and record that path in the linkage layer.
- If state is unclear after interruption, refresh `.wilco/resume/<slug>.md` instead of guessing.
- Treat `.wilco/index/` as a cache-like coordination layer. Keep it minimal and rebuildable from the primary documents.
- When index linkage records slug relationships, use a limited vocabulary such as `related`, `follow_up`, `supersedes`, and `superseded_by`.
- When a slug is split, keep the old slug scoped to its original topic and record the split in both prose and index linkage.
- Treat `.wilco/resume/` as an exception path for recovery, handoff, divergence, or completion checks, not as a default per-slug artifact.
- Prefer archiving promptly once active work is finished so `.wilco/*/active/` stays small and legible.
- Keep `wilco-execute` and `wilco-cleanup` as separate lifecycle stages even when an agent routes through both automatically for the user.

## Recommended Outputs

When asked to design or normalize a docs structure, produce:

- a proposed directory tree
- a lifecycle rule set
- naming rules
- archive criteria
- status block templates if helpful

When asked to archive or complete a document set, produce:

- the target location for each file
- any required status/header updates
- replacement links
- a short explanation of what remains active vs. historical

## References

- For directory layout, naming, and lifecycle conventions, read [references/layout.md](references/layout.md).
- For the decision tree, document levels, lifecycle actions, sync rules, and out-of-sync routing, read [references/decision-tree.md](references/decision-tree.md).
- For archive criteria, status blocks, and completion handling, read [references/archive.md](references/archive.md).
- For automation usage, read [references/automation.md](references/automation.md).
- For shared progress/alignment terms, read [references/status-vocabulary.md](references/status-vocabulary.md).
- For out-of-sync routing and skill combinations, read [references/troubleshooting.md](references/troubleshooting.md).

Keep the active skill body short. Load the reference files only when the user is asking for concrete directory policy, archive mechanics, or status templates.
