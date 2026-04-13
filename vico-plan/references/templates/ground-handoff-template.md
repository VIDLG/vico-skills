# Ground Handoff Template

Use this shape when `vico-ground` hands decisions into `vico-plan`.

```md
Move: handoff

## Ground Handoff

Target

- ...

What is true now

- ...

What is still unresolved

- ...

Recommended route

- `direct_execute` | `vico-plan`

Suggested first step

- ...

Optional: Suggested slug

- ...

Optional: Tracking hint

- `no-doc`
- `plan_only`
- `prd_backed`
```

`vico-plan` should treat these as strong downstream inputs:

- `Target`
- `What is true now`
- `What is still unresolved`
- `Suggested first step`

`Suggested slug` is an optional strong routing hint.

Treat these as soft context inputs:

- `Tracking hint`

Strong downstream inputs should be safe to lean on directly during planning.
Soft context inputs should shape judgment, not silently override repository reality or explicit user input.
