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

Do not maximize document count. Prefer the smallest document set that is sufficient for the task.

## Quick Start

1. Inspect the current `docs/` tree and identify mixed responsibilities, duplicate topics, and historical documents posing as current truth.
2. Classify each document as one of: `prd`, `plan`, `architecture`, `adr`, or `archive`.
3. Decide whether the task needs a plan only, a PRD plus a plan, or a PRD plus a plan plus architecture documentation.
4. Decide whether the task needs a new document, a move, an archive action, or a stable summary document.
5. Make the smallest possible structural change that clarifies ownership and lifecycle.
6. Cross-link replacement documents whenever archiving or superseding older ones.

## Classification Rules

- `PRD`: why the change exists, goals, non-goals, scope, acceptance criteria. In Wilco flows, these normally live under `.wilco/prd/`.
- `Plan`: how to implement the change, phases, migration steps, validation, checklist. In Wilco flows, these normally live under `.wilco/plans/`.
- `Architecture`: the current stable design that future contributors should treat as truth. These should live under `docs/architecture/`.
- `ADR`: a durable architectural decision with context, alternatives, and consequences.
- `Archive`: historical material that is intentionally preserved but no longer drives current work.

Never let `.wilco` planning docs stand in for long-lived architecture truth. If a completed PRD or plan still contains facts contributors will need later, extract those facts into `docs/architecture/` before or alongside archival work.

## Minimal Document Strategy

- Small work: plan only
- Medium work: PRD plus plan
- Large or durable architecture work: PRD plus plan plus architecture

Use PRDs when the intent, scope, or product boundary needs durable explanation. Use plan-only flows when the task is clear enough that a PRD would mostly duplicate the plan.

## Boundary Rules

- `.wilco/` is for active planning, execution tracking, and planning-history artifacts.
- `docs/architecture/` is for current stable truth that should outlive any one plan.
- `docs/adr/` is for key decisions and their rationale, not for current full-system descriptions.
- Do not move planning churn into `docs/architecture/`.
- Do not leave durable truth trapped only in `.wilco/`.

## Working Rules

- Prefer one topic slug across related docs: the same subject should map cleanly across PRD, plan, and architecture files.
- Prefer explicit status over silent historical drift: add `Status`, completion date, and replacement links when archiving.
- Prefer explicit document dates in the header: use stable file names and put `Created`, `Updated`, `Completed`, or review dates in document metadata instead of encoding dates into file names.
- Prefer directory clarity over root-level sprawl: active docs should be easy to distinguish from historical docs at a glance.
- Prefer migration by extraction, not by deletion: move stable truth into architecture docs before retiring planning documents.
- Prefer minimal churn: do not rename or relocate unrelated docs in the same change.

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
- For archive criteria, status blocks, and completion handling, read [references/archive.md](references/archive.md).

Keep the active skill body short. Load the reference files only when the user is asking for concrete directory policy, archive mechanics, or status templates.
