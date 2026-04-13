# Consensus Models

This document summarizes the main theory families behind building shared ground and maps them to the lighter `vico-ground` v2 model.

It is not a second behavior contract for any skill.
Owner contracts still live in each skill's `SKILL.md`.

## Why This Exists

Vico is not only trying to inspect a repo or execute a plan.
It is also trying to help a user and an AI reach a usable shared understanding of:

- what is true enough to act on
- what is still assumed
- what tension still matters
- what route should come next

Theories of common ground are useful here, but `vico-ground` no longer exposes that theory as a large public move set.

## Main Theory Families

### Common Ground

Core idea:
- progress is safer when both sides know what is established and can act on that shared basis

Best Vico mapping:
- `Facts`
- `Assumptions`
- `handoff`

### Conversational Grounding

Core idea:
- dialogue grounds information until it becomes established enough to proceed

Best Vico mapping:
- `clarify`
- explicit uncertainty
- short clarification turns instead of silent guessing

### Sensemaking

Core idea:
- understanding is built iteratively through evidence, interpretation, and reframing

Best Vico mapping:
- `scan`
- optional structural mapping inside `scan`
- repeated narrow evidence gathering

### Collaborative Problem Solving

Core idea:
- dialogue is joint work on a shared problem, not just question answering

Best Vico mapping:
- controller-style routing
- choosing the smallest next move that unlocks action
- stopping once the next route is clear

### Deliberation And Argumentation

Core idea:
- some progress requires structured pressure: claims, evidence, counterexamples, and rebuttals

Best Vico mapping:
- `stress`
- internal `check` / `tradeoff` / `challenge` submodes

### Negotiation And Preference Reconciliation

Core idea:
- not every disagreement is factual; many are preference or constraint conflicts

Best Vico mapping:
- `stress` with tradeoff shape
- explicit priorities and constraints when they affect route choice

### Vocabulary And Ontology Alignment

Core idea:
- people often appear to disagree when they are using the same words differently

Best Vico mapping:
- `clarify`
- restatement of terms and boundaries

### Decision-Making Under Uncertainty

Core idea:
- good workflow decisions manage downside and reversibility instead of pretending to have perfect certainty

Best Vico mapping:
- `handoff`
- route choice under uncertainty
- close-out verification in downstream workflows

### Double-Loop Learning

Core idea:
- strong systems revisit the assumptions and framing that produced the current plan

Best Vico mapping:
- `clarify`
- `scan`
- route shifts when the current frame no longer fits

## Practical Consensus Moves

For `vico-ground` v2, the practical public surface is intentionally small:

- `scan`
  - gather enough evidence to choose the next route
- `clarify`
  - align goals, scope, terms, constraints, or framing
- `stress`
  - pressure-test a proposal, assumption, option set, or plan
- `handoff`
  - stop grounding and make the next route explicit

Internal submodes still exist, but they no longer need to be the main public interface.

## Theory To Move Mapping

| Theory family | Main failure it helps with | Best Vico move | Typical artifact |
| --- | --- | --- | --- |
| Common Ground | people think they agreed when they did not | `clarify`, `handoff` | facts / thin handoff |
| Conversational Grounding | ambiguous statements are treated as established | `clarify` | explicit uncertainty |
| Sensemaking | action starts before the situation is understood well enough | `scan` | evidence / compact conclusions |
| Deliberation / Argumentation | weak proposals survive because they were never pressure-tested | `stress` | tradeoff or challenge notes |
| Preference Reconciliation | factual agreement exists but value conflict remains | `stress` | priorities / constraints |
| Ontology Alignment | the same words hide different meanings | `clarify` | aligned terms / boundaries |
| Decision Under Uncertainty | teams overstate certainty and under-manage risk | `handoff` | route choice / next action |
| Double-Loop Learning | the frame itself is wrong but no one revisits it | `clarify`, `scan` | reframed target |

## Failure Patterns

- hidden assumptions are treated as facts
- preferences are stated as if they were objective truths
- pressure-testing starts before the facts are grounded enough
- grounding continues after the next safe route is already clear
- planning starts before shared ground is strong enough

## Anti-Patterns

- answering the surface wording without checking shared intent
- over-modeling the problem when a smaller route decision is enough
- treating every tension as if it needs a separate public move
- using pressure style as a substitute for route clarity
- exporting operating rules before the current ground is stable enough

## Suggested Shared-Ground State

For the lighter v2 model, the most useful public state buckets are:

- `Facts`
- `Assumptions`
- `Tensions`
- `Next route`

Richer state may still exist internally, but `vico-ground` should not force it into default user-facing output.

## Design Implication For Vico

The most important implication is this:

- `Facts` are not the same thing as `Assumptions`
- `Tension` is not always the same thing as `missing evidence`
- `Consensus` is not the same thing as `full certainty`
- the next safe route matters more than exhausting the current analysis space

That is why `vico-ground` v2 favors a small public move set, thin handoffs, and strong stop rules instead of a large visible grounding taxonomy.
