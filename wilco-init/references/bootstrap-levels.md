# Bootstrap Levels

Use the smallest level that keeps the work clear.

## Levels

- `no-doc`: do not create Wilco artifacts
- `plan-only`: create the active plan and the derived index manifest
- `prd-plan`: create both PRD and plan
- `prd-plan-arch`: create PRD, plan, and an architecture document only when durable truth should exist immediately

## Default Rule

- default to `plan-only`
- escalate to `prd-plan` only when scope or acceptance needs durable explanation
- escalate to `prd-plan-arch` only when durable architecture truth should be captured immediately
