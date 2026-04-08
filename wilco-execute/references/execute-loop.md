# Execute Loop

Use this loop for persistent execution.

## Step 1: Confirm the active source

- Prefer `.wilco/plans/active/<slug>.md`
- If a `wilco-resume` report exists and is current, use it to choose the next step

## Step 2: Reconcile if needed

Before executing, confirm the plan still matches current code and tests closely enough.

If not:
- run `wilco-resume`
- update the working understanding
- then continue

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

## Step 7: Continue or stop

Continue when:

- there is another unblocked step
- no user decision is needed

Stop when:

- all planned work is complete
- a real blocker exists
- a decision is needed from the user
- continuing would require guessing beyond the current plan or PRD

## Required Output At Any Stop Point

- what was completed
- current verification result
- exact blocker or stopping reason
- the next recommended step
