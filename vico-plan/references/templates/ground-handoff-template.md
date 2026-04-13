# Ground Handoff Template

Use this shape when `vico-ground` hands decisions into `vico-plan`.

```md
## Ground Handoff

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
- Optional: Active assumptions
  - ...
- Optional: Preferences
  - ...
- Optional: Tradeoffs
  - ...
- Optional: Commitments
  - ...
- Optional: Resolved during grounding
  - ...
- Unresolved decisions
  - ...
- Suggested edits
  - ...
- Optional: Invalidation triggers
  - ...
- Optional: Recommended resolutions
  - ...
- Optional: Edit priority
  - ...
```

`vico-plan` should treat these as strong downstream inputs:

- `Target`
- `Accepted decisions`
- `Unresolved decisions`
- `Suggested edits`

`Slug` and `Issue classes` are optional strong routing hints.

Treat these as soft context inputs:

- `Active assumptions`
- `Preferences`
- `Tradeoffs`
- `Commitments`
- `Resolved during grounding`
- `Recommended tracking mode`
- `Suggested first slice`
- `Execution readiness risks`
- `Invalidation triggers`
- `Recommended resolutions`
- `Edit priority`

Strong downstream inputs should be safe to lean on directly during planning.
Soft context inputs should shape judgment, not silently override repository reality or explicit user input.
