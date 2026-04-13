## Claude Runner

Use the bundled runner when Claude Code needs a stronger outer loop than hooks alone.

The runner repeatedly calls `claude -p`, asks Claude Code to execute one `vico-exec` pass, requires structured JSON status, and decides whether to loop again.

## Intended Use

- plan already exists under `.vico/plans/active/`
- Claude Code is the execution agent
- you want an outer loop that keeps going until:
  - execution is done
  - a real blocker exists
  - a user decision is needed
  - the plan is stale enough that `vico-plan` should re-enter

## Command

```bash
python3 vico-skills/vico-exec/scripts/claude_exec_runner.py --repo-root D:/projects/spoon
```

When more than one active plan exists, pass `--slug`:

```bash
python3 vico-skills/vico-exec/scripts/claude_exec_runner.py --repo-root D:/projects/spoon --slug 2026-04-12-example
```

Useful options:

- `--max-iterations 20`
- `--model sonnet`
- `--effort high`
- `--permission-mode acceptEdits`
- `--bare`
- `--dangerously-skip-permissions`

## Runner Actions

Claude must return exactly one of:

- `continue`
- `done`
- `blocked`
- `needs_user`
- `stale_plan`

`done` means the current execution looks complete and verification found no material open gaps.
`stale_plan` means stop looping and route back through `vico-plan`.

## Notes

- use hooks when you only want lightweight execution discipline
- use the runner when you want an explicit repeat-until-stop loop
- the runner does not perform close-out deletion
- after `done`, prefer `vico-plan verify` or `vico-plan close` based on user intent
- see [cc-operator.md](cc-operator.md) for the recommended human operator flow around exit codes and reruns
