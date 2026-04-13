# Vico Ground Output Format

Use this file for worked examples and anti-examples.
Start with `index.md` for the full reference map.

## Scan Example

```md
Move: scan

Conclusion

- The repo already has a stable planning and execution split.
- The main design pressure is that `vico-ground` still exposes too many public moves.

Evidence

- `vico-plan` and `vico-exec` already own tracked planning and persistent execution.
- `vico-ground` docs currently expose many adjacent move names for similar kinds of work.

Why this matters

- the next step should be controller simplification rather than more grounding depth

Next route

- `vico-plan`

Recommended next action

- rewrite the `vico-ground` public contract around fewer moves and a thinner handoff

Other next actions

- draft the routing deltas before editing templates
- run `vico-ground stress` on the proposed simplification first
```

## Clarify Example

```md
Move: clarify

Conclusion

- The real ambiguity is not implementation scope.
- The real ambiguity is whether the user wants repository orientation or immediate code changes.

Evidence

- the request asks for a scan of the overall project rather than a narrow file edit
- no concrete implementation target was named

Next route

- `stay_in_ground`

Recommended next action

- continue with `vico-ground scan`

Other next actions

- ask one short clarification question if the target is still ambiguous
- route directly to `direct_execute` if the user narrows to one local change
```

## Stress Example

```md
Move: stress

Conclusion

- Keeping `tradeoff`, `grill`, and `challenge` as separate public moves adds more routing cost than user value.

Evidence

- all three operate on pressure rather than on distinct workflow stages
- most practical requests only need one pressure-testing entrypoint

Next route

- `stay_in_ground`

Recommended next action

- collapse those routes into `vico-ground stress`

Other next actions

- keep the public route names but reduce them to aliases only
- prototype the shorter route set in help docs before rewriting the skill contract
```

## Handoff Example

```md
Move: handoff

Conclusion

- The next safe route is tracked planning.
- Further grounding would mostly restate the same design conclusions.

Evidence

- the redesign goals are clear enough to plan concrete document changes
- the remaining work is execution shaping, not more framing

Next route

- `vico-plan`

Recommended next action

- create the v2 migration plan and update the skill contract

Other next actions

- open a `vico-plan` replan pass focused on the handoff contract
- capture one thin handoff example before touching the main contract
```

## Full Handoff Example

```md
Move: handoff

## Ground Handoff

Target

- redesign `vico-ground` as a lighter pre-planning controller

What is true now

- the public move surface is too wide
- the default output contract is heavier than most scans need

What is still unresolved

- whether `stress` needs a shorter alias in natural-language usage

Recommended route

- `vico-plan`

Suggested first step

- rewrite `vico-ground/SKILL.md` around `scan`, `clarify`, `stress`, and `handoff`

Tracking hint

- `plan_only`
```

## Incomplete Anti-Example

This example is intentionally incomplete. It should not be treated as a valid output because it names a concern but does not route forward.

```md
Move: scan

Conclusion

- The docs feel too heavy.

Evidence

- There are many sections.
```

Why this is incomplete:

- missing `Next route`
- missing `Recommended next action`
- does not hand the work forward
