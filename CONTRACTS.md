# Wilco Contracts

This document is a governance map. It does not become a new source of workflow, skill, or template truth.

## Distribution Assumptions

- Runtime should be safe for single-skill installation and use.
- Runtime must not depend on the repository-root `README.md`.
- Runtime must not depend on cross-skill paths such as `../wilco-docs/...`.
- Shared runtime needs must be satisfied through owner sources plus skill-local closures.

## Contract Layers

1. `Global workflow constitution`
   Owner source: [README.md](README.md)
2. `Skill behavior contracts`
   Owner source: each `<skill>/SKILL.md`
3. `Shared structural contracts`
   Owner sources: the owning template, reference, or shared-script source file

## Owners And Derived Forms

| Contract type | Owner source | Derived forms | Validator responsibility |
| --- | --- | --- | --- |
| Global workflow constitution | `README.md` | skill-level references, contract map entries, workflow invariant checks | ensure README markers exist and downstream docs do not drift on core invariants |
| Skill behavior contract | each `<skill>/SKILL.md` | `<skill>/agents/openai.yaml`, skill-local references, examples | ensure the skill body is present, referenced helpers exist, and agent summaries do not become a second full contract |
| Shared scripts | owner script file, currently under `wilco-docs/scripts/` | skill-local wrapper entries under `<skill>/scripts/` | ensure owner source exists, local wrapper entry points exist where required, and runtime references do not point across skill boundaries |
| Shared status and decision rules | owner reference file, such as `wilco-docs/references/status-vocabulary.md` or `decision-tree.md` | skill-local full reference copies where runtime visibility is required | ensure owner files exist, local copies exist where required, and copies are treated as derived content |
| Strong templates | owner template file, such as `plan-template.md`, `prd-template.md`, `resume-output-template.md` | skill-local visible copies or references needed for runtime closure | ensure owner templates exist, required local closures exist, and key structure remains stable |
| Contract map | `CONTRACTS.md` and `CONTRACTS-zh.md` | README links | ensure the map exists and keeps owner/derived/validation responsibilities aligned |

## Sync Policy

- Owner sources are edited directly.
- Derived forms are synchronized from owner sources.
- Derived forms are read-only by default.
- If a derived file needs owner-specific additions, the derived block and the owner-local block must be explicitly separated.
- Do not create a new top-level shared source directory just to deduplicate content.
- Only synchronize high-repeat, structurally stable, cross-skill content.

### First Migration Order

1. shared scripts
2. status and decision rules
3. strong structural templates

## Validation Responsibilities

Validator checks should be explicit rather than generic. At minimum they should cover:

- owner source existence
- derived-form presence
- sync-boundary enforcement
- read-only generated content rules

## Notes

- This document maps ownership and synchronization. It does not replace the owner files.
- When a contract changes, update the owner source first, then refresh derived forms, then update validator coverage.
