---
name: wilco-docs-governance
description: Repository documentation governance for Wilco-style engineering docs. Use when organizing or evolving repo-local PRDs, implementation plans, architecture docs, ADRs, and archive folders; deciding where docs belong; defining document lifecycle rules; archiving completed plans or PRDs; or separating current architecture truth from historical planning records.
---

# Docs Governance

## Overview

Treat engineering documentation as a lifecycle, not a pile of markdown files. Keep current truth in stable docs, keep execution history in archived PRDs and plans, and make document status explicit whenever a document stops being active.

## Quick Start

1. Inspect the current `docs/` tree and identify mixed responsibilities, duplicate topics, and historical documents posing as current truth.
2. Classify each document as one of: `prd`, `plan`, `architecture`, `adr`, or `archive`.
3. Decide whether the task needs a new document, a move, an archive action, or a stable summary document.
4. Make the smallest possible structural change that clarifies ownership and lifecycle.
5. Cross-link replacement documents whenever archiving or superseding older ones.

## Classification Rules

- `PRD`: why the change exists, goals, non-goals, scope, acceptance criteria.
- `Plan`: how to implement the change, phases, migration steps, validation, checklist.
- `Architecture`: the current stable design that future contributors should treat as truth.
- `ADR`: a durable architectural decision with context, alternatives, and consequences.
- `Archive`: historical material that is intentionally preserved but no longer drives current work.

Never let archived PRDs or plans stand in for current architecture. If a completed plan still contains facts contributors need, extract those facts into an architecture document before or alongside archival work.

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
