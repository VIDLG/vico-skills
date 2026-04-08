# wilco-skills

Custom repository-oriented Codex skills.

Current skills:

- `wilco-docs`
- `wilco-execute`
- `wilco-grill`
- `wilco-prd`
- `wilco-plan`
- `wilco-resume`

Workflow map:

- `wilco-prd` -> create `.wilco/prd/active/<slug>.md` when the work is large enough to justify a PRD
- `wilco-plan` -> create `.wilco/plans/active/<slug>.md` from a PRD or as a plan-only document for smaller work
- `wilco-grill` -> stress-test the current PRD, plan, or design
- `wilco-resume` -> reconcile PRD/plan/code or plan/code and determine the true next step
- `wilco-execute` -> keep executing the active plan until done or a real blocker exists
- `wilco-docs` -> govern the boundary between `.wilco/` planning docs and `docs/` long-lived truth

Intended distribution model:

- keep each skill in a standalone folder with `SKILL.md`
- stay compatible with public skill-repo conventions
- support installation workflows for both Claude Code and Codex

Development usage:

- Treat `wilco-skills/` as the single source of truth.
- During development, point project-local `.codex/skills/` and `.claude/skills/` entries at these folders instead of copying skill contents.
- For Claude Code, hook scripts live in `wilco-execute/scripts/` and project hook wiring lives in `.claude/settings*.json`.
