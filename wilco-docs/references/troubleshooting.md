# Out-Of-Sync Triage

When `.wilco` artifacts disagree with code or with each other, start with `wilco-resume`.

## Default Rule

- trust code and tests over stale checklist state
- use `wilco-resume` to decide what is stale before editing documents
- then route to the smallest follow-up skill set

## Skill Routing

- this is brand-new work and no slug exists yet:
  use `wilco-init`
- execution state stale, checklist stale, or source paths stale:
  use `wilco-resume` then `wilco-plan`
- scope, goals, non-goals, or acceptance changed:
  use `wilco-resume` then `wilco-prd` and `wilco-plan`
- architecture truth moved but docs did not:
  use `wilco-resume` then `wilco-docs`
- task is effectively done but active docs still linger:
  use `wilco-resume` then `wilco-cleanup`
- you only need to continue after interruption:
  use `wilco-resume` then `wilco-execute`
- implementation is complete and the user asked to finish end-to-end:
  use `wilco-execute` then `wilco-cleanup`

## Automation Follow-Up

- if you are just creating the first artifact set, run `../wilco-init/scripts/bootstrap_wilco_slug.py`
- if headers drifted, run `scripts/sync_wilco_headers.py`
- if the current linkage file is stale, run `scripts/sync_wilco_index.py`
- if the work is complete, run `scripts/close_wilco_slug.py` from the cleanup stage after the final reconciliation
