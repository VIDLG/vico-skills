# Resume Checklist

Use this checklist when comparing PRD, plan, and code.

## PRD Checks

- What problem is the PRD trying to solve?
- What outcomes are explicitly in scope?
- What is explicitly out of scope?
- What decisions in the PRD still appear to matter?
- Does the PRD still add independent scope, intent, or acceptance value beyond the plan?

## Plan Checks

- What phases exist?
- What acceptance criteria exist per phase?
- Which architectural decisions are supposed to be durable?
- What current status or progress markers are already in the plan?

## Code And Test Checks

- Are the intended entrypoints present?
- Are the relevant modules present, moved, or deleted?
- Are focused tests present near the logic?
- Do regression or flow tests indicate the behavior exists?
- Are there compatibility shims or stale adapters still left behind?
- Are there obvious TODO/FIXME notes that indicate unfinished work?

## Classification Rules

- `done`: code and tests support that the acceptance intent is implemented.
- `partial`: some of the intended behavior exists, but not enough to call complete.
- `not_started`: no meaningful implementation evidence exists.
- `diverged`: implementation exists, but the structure or behavior no longer matches the plan.
- `unclear`: available evidence is insufficient for a reliable conclusion.

## Document Update Guidance

- Update the plan if checklist state or source references are stale.
- Update the PRD only if the intended scope or problem framing has actually changed.
- Recommend `downgrade-to-plan-only` if the PRD has become redundant.
- Add or update architecture docs when current stable truth is only implied by code or buried in old plans.
- If the topic split into a new slug, record the split in prose and index linkage instead of silently stretching the old slug.
- Remove or clear stale resume linkage once the plan is current again and no further handoff is needed.

## Resume Staleness Checks

- Did the linked PRD update after the current resume?
- Did the linked plan update after the current resume?
- Did checklist state change after the current resume was written?
- Does current code or test evidence clearly exceed or contradict the old resume?

If yes, overwrite the current resume file instead of trusting the old one.
