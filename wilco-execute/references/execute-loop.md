# Execute Loop

Use this loop for persistent execution.

## Step 1: Confirm the active source

- Prefer `.wilco/index/<slug>.json`
- Resolve the current plan and current resume from the manifest when available
- If a `wilco-resume` report exists and is current, use it to choose the next step
- Treat the plan as the durable source for ongoing execution; treat resume as a temporary handoff or recovery snapshot

## Step 2: Reconcile if needed

Before executing, confirm the plan still matches current code and tests closely enough.

If not:
- run `wilco-resume`
- update the working understanding
- then continue

Also rerun `wilco-resume` if the current resume is stale relative to the linked plan or PRD.
If no handoff, recovery, divergence, or closure check is needed, do not create or refresh a resume file.

## Step 3: Pick the next smallest unblocked step

Choose:

- the smallest remaining acceptance criterion
- or the smallest plan slice that can be implemented and verified

Do not pick a larger batch just because it feels more efficient.
Treat the plan checklist as the primary execution anchor. If a recent resume report exists, use it to choose the correct next unchecked or partially completed item.

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
- if a temporary resume was used, either delete it once the plan is current again or clearly leave it only until the next handoff
- if an index manifest points to a removed resume file, clear that linkage

## Step 7: Continue or stop

Continue when:

- there is another unblocked step
- no user decision is needed
- no stale-plan or stale-resume condition requires fresh reconciliation

Stop when:

- all planned work is complete
- a real blocker exists
- a decision is needed from the user
- continuing would require guessing beyond the current plan or PRD

When all planned work is complete:

- update the plan so completion is explicit
- if the user expects end-to-end completion, route directly to `wilco-cleanup`
- do not perform archive handling inside `wilco-execute`

## Required Output At Any Stop Point

- what was completed
- current verification result
- exact blocker or stopping reason
- the next recommended step

## Resume Cleanup Rule

After a successful execution pass, prefer this order:

1. update the plan so it reflects reality
2. keep or refresh resume only if another handoff or reconciliation is still needed
3. otherwise remove the temporary resume file and clear any stale index linkage
