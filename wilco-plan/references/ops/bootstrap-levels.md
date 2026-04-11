# Bootstrap Levels

`wilco-plan` may internally bootstrap new tracked work when no clean active slug exists.

Use the smallest level that keeps the work clear.

## Levels

- `no-doc`: do not create Wilco artifacts
- `plan_only`: create the active plan and the derived index manifest
- `prd_backed`: create both PRD and plan
- `prd_backed_arch`: create PRD, plan, and an architecture document only when durable truth should exist immediately

## Default Rule

- default to `plan_only`
- escalate to `prd_backed` only when scope or acceptance needs durable explanation
- escalate to `prd_backed_arch` only when durable architecture truth should be captured immediately
