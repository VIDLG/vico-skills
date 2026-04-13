# Consensus Models

This document summarizes the main theory families behind "building shared ground" and shows how they map into Vico workflows.

It is not a second behavior contract for any skill.
Owner contracts still live in each skill's `SKILL.md`.

## Why This Exists

Vico is not only trying to inspect a repo or execute a plan.
It is also trying to help a user and an AI reach a usable shared understanding of:

- what is true
- what is assumed
- what is still contested
- what tradeoffs matter
- what should happen next

That shared understanding has a theory background.

## Main Theory Families

### Common Ground

Core idea:
- communication succeeds when both sides know something, know that the other knows it, and can act on that shared basis

What it explains:
- why accepted facts and accepted decisions should be tracked explicitly
- why hidden assumptions and silent ambiguity break collaboration

Best Vico mapping:
- `Accepted Facts`
- `Accepted Decisions`
- `Active Assumptions`
- `Open Questions`
- `Ground / Probe Handoff`

### Conversational Grounding

Core idea:
- dialogue is a process of grounding information until it becomes mutually established enough to proceed

What it explains:
- why not every statement is equally "established"
- why a skill should distinguish between proposed, assumed, accepted, and unresolved content

Best Vico mapping:
- clarification-first behavior
- explicit uncertainty
- short clarification turns instead of silent guessing

### Sensemaking

Core idea:
- in complex situations, people build understanding iteratively by gathering signals, forming interpretations, and revising the frame

What it explains:
- why `scan` should first establish the problem map instead of jumping into action
- why findings, issues, and topic maps should evolve over time

Best Vico mapping:
- `Evidence Bank`
- `Findings`
- `Issue Bank`
- `Topic Map`
- repeated narrow `scan`

### Collaborative Problem Solving

Core idea:
- dialogue is not just question answering; it is joint work on a shared problem

What it explains:
- why modes like `clarify`, `review`, and `resolve` should be treated as different joint moves rather than different output skins

Best Vico mapping:
- controller-style routing
- move selection based on what the collaboration needs next

### Deliberation And Argumentation

Core idea:
- some progress requires structured challenge: surfacing claims, evidence, assumptions, counterexamples, and rebuttals

What it explains:
- why `grill` should not be generic questioning
- why tradeoffs and counterexamples matter

Best Vico mapping:
- `grill`
- `tradeoff`
- `challenge`
- `counterexample`
- explicit recommendation vs. open branch

### Negotiation And Preference Reconciliation

Core idea:
- not every disagreement is factual; many disagreements are preference or constraint conflicts

What it explains:
- why facts alone do not settle plan shape, documentation burden, or rollout order
- why the system should sometimes reconcile priorities instead of just collecting evidence

Best Vico mapping:
- `tradeoff`
- hard vs. soft constraints
- preference ranking
- execution-risk negotiation

### Vocabulary And Ontology Alignment

Core idea:
- people often appear to disagree when they are actually using the same words with different meanings

What it explains:
- why terms like `done`, `verify`, `tracked`, `architecture`, or `simple` need explicit alignment

Best Vico mapping:
- `align`
- term freeze
- boundary naming
- restatement and glossary behavior

### Decision-Making Under Uncertainty

Core idea:
- many workflow decisions are made under incomplete evidence, so good systems optimize for acceptable risk rather than perfect certainty

What it explains:
- why Vico should weigh reversibility, downside, ambiguity, and verification strength

Best Vico mapping:
- recommendation shortcuts
- execution readiness
- close-out verification
- continue vs. stale-plan vs. needs-user routing

### Double-Loop Learning

Core idea:
- strong systems do not only fix actions; they also revisit the assumptions, goals, and process that produced the action

What it explains:
- why process review and mode shifts are part of building consensus
- why the workflow sometimes needs to question its own frame

Best Vico mapping:
- process review
- route shift
- reframe
- assumption audit

## Practical Consensus Moves

These are the most usable "moves" that fall out of the theories above:

- `clarify`
  align goals, terms, scope, and success criteria
- `scan`
  build evidence, findings, issues, and a topic map
- `align`
  explicitly normalize meanings and boundaries
- `tradeoff`
  compare options, priorities, and irreversibilities
- `grill`
  pressure-test assumptions and conclusions
- `map`
  externalize the current structure of the problem
- `review`
  checkpoint current shared ground without expanding it
- `resolve`
  compress the current shared ground into a decision or handoff

## Theory To Move Mapping

| Theory family | Main failure it helps with | Best Vico moves | Typical grounded artifact |
| --- | --- | --- | --- |
| Common Ground | people think they agreed when they did not | `clarify`, `review`, `resolve` | accepted facts / accepted decisions |
| Conversational Grounding | ambiguous statements are treated as established | `clarify`, `align` | epistemic status separation |
| Sensemaking | action starts before the situation is structurally understood | `scan`, `map`, `reframe` | findings / topic map |
| Deliberation / Argumentation | weak proposals survive because they were never pressure-tested | `grill`, `challenge` | tradeoffs / rebuttals |
| Preference Reconciliation | factual agreement exists but value conflict remains | `tradeoff` | explicit priorities / constraints |
| Ontology Alignment | the same words hide different meanings | `align` | accepted vocabulary / boundaries |
| Decision Under Uncertainty | teams overstate certainty and under-manage risk | `tradeoff`, `review`, `resolve` | assumptions / commitments / risks |
| Double-Loop Learning | the frame itself is wrong but no one revisits it | `reframe`, `review` | replacement frame / updated objective |

## Failure Patterns

- hidden assumptions are treated as facts
- preferences are stated as if they were objective truths
- findings are dumped as if they were the full issue set
- disagreement is mislabeled as missing evidence
- a weak frame is pressure-tested instead of reframed
- planning starts before shared ground is strong enough

## Anti-Patterns

- answering the user's surface wording without checking shared intent
- collapsing all uncertainty into one generic `open question`
- treating every finding as an issue
- using `grill` when the real need is `tradeoff` or `align`
- using `challenge` as a style of aggression instead of a structured review move
- exporting operating rules before the current ground is stable enough

## Suggested Shared-Ground State

If Vico evolves toward a stronger consensus model, these are the most useful state buckets:

- `Objective`
- `Target`
- `Accepted Facts`
- `Accepted Decisions`
- `Active Assumptions`
- `Disagreements`
- `Tradeoffs`
- `Open Questions`
- `Evidence Bank`
- `Findings`
- `Issue Bank`
- `Topic Map`
- `Ground Handoff`

## Design Implication For Vico

The most important implication is this:

- `Findings` are not the same thing as `Issues`
- `Facts` are not the same thing as `Assumptions`
- `Disagreement` is not always the same thing as `missing evidence`
- `Consensus` is not the same thing as `full certainty`

That is why Vico benefits from separate moves, separate state buckets, and explicit handoff contracts instead of a single generic "analyze" step.
