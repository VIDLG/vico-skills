# Claude Hook Setup

These hooks are optional helpers for Claude Code.
If you need a stronger outer loop, use [runner.md](runner.md) instead of relying on hooks alone.

Goal:

- remind Claude of the active Vico plan at session start
- discourage stopping when active work remains and no real blocker was reported

## Suggested Wiring

Use `.claude/settings.local.json` to point Claude hooks at the scripts in this skill directory.

Suggested events:

- `SessionStart` -> `scripts/session_start_hook.ps1`
- `Stop` -> `scripts/stop_hook.ps1`

## Important Notes

- Hooks should reinforce execution discipline, not replace reasoning.
- Hooks are lighter-weight than the bundled Claude runner loop.
- Do not use hooks to silently invent progress.
- Let the model stop when a real blocker exists or a user decision is needed.
- After changing Claude hooks, start a new session or re-review the hooks configuration so the new settings take effect.

## Example Intent

- `SessionStart`: emit a reminder to anchor execution on `.vico/plans/active/`
- `Stop`: if active plan work likely remains and no blocker summary was produced, ask Claude to continue or explain the blocker more explicitly
