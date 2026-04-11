# Blocker Taxonomy

Classify blockers explicitly instead of saying only "blocked".

- `user_decision`: the plan cannot proceed without a user choice.
- `stale_plan`: the plan is no longer reliable enough to execute directly.
- `verification_failure`: code changed, but verification failed and the next move is unclear.
- `external_dependency`: network, toolchain, credentials, or environment dependency is missing.
- `worktree_conflict`: unrelated user or generated changes make continuation unsafe.

When blocked, report:

- blocker type
- exact evidence
- what input or change would unblock execution

## Blocked Output Shape

Use this compact shape when execution stops on a blocker.

```md
## Blocked

- Type: `user_decision` | `stale_plan` | `verification_failure` | `external_dependency` | `worktree_conflict`
- Evidence: ...
- Unblock: ...
- Next step: ...
```
