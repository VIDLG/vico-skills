# Probe Handoff Template

Use this shape when `wilco-probe` hands decisions into `wilco-plan`.

```md
## Probe Handoff

- Target
  - ...
- Optional: Slug
  - ...
- Optional: Issue classes
  - intent
  - execution
  - durable_truth
- Optional: Recommended tracking mode
  - `plan_only`
  - `prd_backed`
- Optional: Suggested first slice
  - ...
- Optional: Execution readiness risks
  - ...
- Accepted decisions
  - ...
- Optional: Resolved during probe
  - ...
- Unresolved decisions
  - ...
- Suggested edits
  - ...
- Optional: Recommended resolutions
  - ...
- Optional: Edit priority
  - ...
```

`wilco-plan` should treat these as strong inputs:

- `Target`
- `Accepted decisions`
- `Unresolved decisions`
- `Suggested edits`

`Slug` and `Issue classes` are optional strong routing hints.
`Resolved during probe`, `Recommended tracking mode`, `Suggested first slice`, `Execution readiness risks`, `Recommended resolutions`, and `Edit priority` are soft inputs.
