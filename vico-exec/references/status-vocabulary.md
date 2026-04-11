# Status Vocabulary

Use one shared vocabulary across Vico skills.

## Work Status

- `done`: implementation and verification support the conclusion that the target is complete.
- `partial`: some meaningful implementation exists, but the target is not complete.
- `not_started`: no meaningful implementation evidence exists yet.
- `diverged`: implementation exists, but no longer matches the plan or expected structure closely enough.
- `unclear`: available evidence is insufficient for a reliable conclusion.

## Execution Progress

- `not_started`: tracked work exists, but no meaningful execution progress has landed yet.
- `partially_completed`: some planned work is landed, but the slug is still in an early or middle stage.
- `mostly_complete`: only a small remainder or explicit cleanup stream is left.
- `done`: the tracked work is complete and ready for close-out cleanup.

## Alignment Status

- `aligned`: PRD, plan, and implementation are materially consistent.
- `partially_aligned`: the general direction matches, but there are stale or incomplete mismatches.
- `diverged`: the implementation no longer tracks the documented plan or intent closely enough.

## Confidence

- `high`: strong code and/or test evidence supports the conclusion.
- `medium`: some evidence exists, but not enough to remove important uncertainty.
- `low`: the conclusion is tentative because evidence is sparse or indirect.
