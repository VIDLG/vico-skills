# Vico Ground Output Format

## Scan Example

```md
repo | architecture > current-understanding
Mode: concise | available: concise, detailed
Priority: critical

Findings

- [critical] Build boundary is currently spread across two orchestration layers.
- [important] Completion terminology is used inconsistently between docs and code.
- [detail] Findings and issues should stay distinct in user-facing scan output.

Evidence

- `runner` logic exists in execution docs but not yet in the shared mental model of every agent.
- Several workflow terms are overloaded across README and skill contracts.

Topic map snapshot

- execution-surface: active
- vocabulary-alignment: active
- export-flow: deferred

High-risk gaps

- completion and close-out are still easy to conflate

Likely recommendations

- align the public vocabulary before expanding execution automation

Open questions worth asking

- Should `challenge` and `grill` stay distinct public moves, or should one become a stronger submove of the other?

Suggested next move

- `tradeoff`
```

## Ground Handoff Example

```md
## Ground Handoff

- Target
  - repo workflow redesign
- Accepted facts
  - `Findings` and `Issues` should remain distinct
  - the execution side now includes a Claude Code runner loop
- Accepted decisions
  - shared-ground construction is broader than repo inspection
  - adversarial pressure-testing should remain an explicit move
- Active assumptions
  - `vico-ground` should become the umbrella workflow name
- Preferences
  - keep the public command surface small even when the internal move system grows
- Tradeoffs
  - larger state model improves clarity but increases contract surface
- Commitments
  - route grounding into planning only after the current frame is stable enough to execute from
- Open questions
  - whether older terms should be removed immediately or staged out
- Invalidation triggers
  - if users still confuse `grill` and `challenge`, tighten their public contracts again
- Recommended next action
  - `vico-plan`
```
