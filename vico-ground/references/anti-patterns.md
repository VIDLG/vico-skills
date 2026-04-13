# Vico Ground Anti-Patterns

Use this page as a quick checklist of common execution failures.
Keep `SKILL.md` authoritative when this page and the main contract differ.

## Output Anti-Patterns

- `scan` that expands into a full architecture memo
  - gathers far more detail than is needed to choose the next route
  - produces structure without improving actionability

- `clarify` that keeps asking questions after the next route is already obvious
  - uses interaction to perfect wording instead of unlocking action

- `stress` that argues without changing the next decision
  - produces rebuttals or option lists with no route consequence

- `handoff` that restarts analysis instead of stopping grounding
  - keeps discovering instead of routing
  - hides the route under summary prose

## Move Selection Anti-Patterns

- using a larger move only because it sounds more rigorous
- exposing internal submodes such as `tradeoff` or `challenge` as if they were the public interface
- using `scan` when the real gap is scope or terminology
- using `clarify` when the missing piece is factual repository evidence
- using `stress` before the facts or options are grounded enough to pressure-test

## Framing Anti-Patterns

- presenting assumptions as facts
- presenting one interpretation as if it were the only possible frame
- carrying old route names forward as if they were still the preferred public surface

## Recovery Rule

- if the move has drifted, name the drift explicitly and switch to the smallest sufficient correct move
- if the next safe route is already clear, stop grounding and emit `handoff`
