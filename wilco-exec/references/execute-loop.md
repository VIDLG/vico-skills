# Execute Loop

Use this loop for persistent execution.

## Step 1: Confirm the active source

- Prefer `.wilco/index/<slug>.json`
- Resolve the current plan and any temporary reconcile state from the manifest when available
- If a temporary reconcile block exists and is current, use it to choose the next step
- Treat the plan as the durable source for ongoing execution; treat temporary reconcile state as an exception path

## Step 2: Reconcile if needed

Before executing, confirm the plan still matches current code and tests closely enough.

If not:
- route back through `wilco-plan`
- update the working understanding
- then continue

If no handoff, recovery, divergence, or closure check is needed, do not create or refresh temporary reconcile state.

## Step 3: Pick the next smallest unblocked step

Choose:

- the smallest remaining acceptance criterion
- or the smallest plan slice that can be implemented and verified

Do not pick a larger batch just because it feels more efficient.
Treat the plan checklist as the primary execution anchor. If a recent temporary reconcile block exists, use it to choose the correct next unchecked or partially completed item.

## Step 4: Execute

- make the minimal code or doc changes needed
- avoid unrelated cleanup
- preserve plan alignment unless deliberate divergence is necessary

## Step 5: Verify

- run the narrowest meaningful verification first
- expand verification only when risk or coupling requires it

## Step 6: Update state

If the user expects docs to stay current:

- update plan checklist state
- update `Updated` date
- record divergences if implementation no longer matches the plan exactly
- if temporary reconcile state was used, either delete it once the plan is current again or clearly leave it only until the next handoff
- if an index manifest points to removed temporary reconcile state, clear that linkage

## Step 7: Continue or stop

Continue when:

- there is another unblocked step
- no user decision is needed
- no stale-plan or stale-reconcile condition requires fresh reconciliation

Stop when:

- all planned work is complete
- a real blocker exists
- a decision is needed from the user
- continuing would require guessing beyond the current plan or PRD

When all planned work is complete:

- update the plan so completion is explicit
- if the user expects end-to-end completion, route directly to `wilco-plan done`
- do not perform close-out deletion inside `wilco-exec`

## Required Output At Any Stop Point

- what was completed
- current verification result
- exact blocker or stopping reason
- the next recommended step

## Resume Cleanup Rule

After a successful execution pass, prefer this order:

1. update the plan so it reflects reality
2. keep or refresh temporary reconcile state only if another handoff or reconciliation is still needed
3. otherwise remove that temporary state and clear any stale index linkage
