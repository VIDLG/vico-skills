#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


RUNNER_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "runner_action": {
            "type": "string",
            "enum": ["continue", "done", "blocked", "needs_user", "stale_plan"],
        },
        "summary": {"type": "string"},
        "verification": {"type": "string"},
        "next_step": {"type": "string"},
        "recommended_command": {"type": "string"},
    },
    "required": [
        "runner_action",
        "summary",
        "verification",
        "next_step",
        "recommended_command",
    ],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a Claude Code outer loop for vico-exec until completion, blocker, user input, or stale-plan stop."
    )
    parser.add_argument("--repo-root", default=".", help="Repository root that contains .vico/")
    parser.add_argument("--slug", help="Exact active plan slug without .md when multiple active plans exist")
    parser.add_argument("--claude-command", default="claude", help="Claude CLI command to invoke")
    parser.add_argument("--max-iterations", type=int, default=12, help="Maximum Claude loop iterations")
    parser.add_argument("--model", help="Claude model alias or full name")
    parser.add_argument("--effort", default="medium", help="Claude effort level")
    parser.add_argument(
        "--permission-mode",
        default="default",
        choices=["default", "acceptEdits", "auto", "bypassPermissions", "dontAsk", "plan"],
        help="Claude permission mode for each loop iteration",
    )
    parser.add_argument("--add-dir", action="append", default=[], help="Additional directories to allow tool access to")
    parser.add_argument("--bare", action="store_true", help="Run Claude in bare mode")
    parser.add_argument(
        "--dangerously-skip-permissions",
        action="store_true",
        help="Pass Claude's dangerous skip permissions flag",
    )
    return parser.parse_args()


def resolve_active_plan(repo_root: Path, slug: str | None) -> Path:
    plan_root = repo_root / ".vico" / "plans" / "active"
    if not plan_root.exists():
        raise SystemExit(f"No active plan directory found at {plan_root}")

    if slug:
        candidate = plan_root / f"{slug}.md"
        if not candidate.exists():
            raise SystemExit(f"Active plan not found for slug '{slug}' at {candidate}")
        return candidate.resolve()

    plans = sorted(plan_root.glob("*.md"))
    if not plans:
        raise SystemExit(f"No active plan found under {plan_root}")
    if len(plans) > 1:
        names = ", ".join(path.stem for path in plans)
        raise SystemExit(f"Multiple active plans found ({names}). Re-run with --slug.")
    return plans[0].resolve()


def build_prompt(repo_root: Path, plan_path: Path) -> str:
    relative_plan = plan_path.relative_to(repo_root).as_posix()
    return f"""You are running inside a repo-local Vico exec runner loop for Claude Code.

Target plan: {relative_plan}

Execute one strong vico-exec pass against that target.

Requirements:
- follow the repository's AGENTS.md plus the vico-skills vico-exec contract
- reconcile against current repository reality before trusting stale plan state
- implement the smallest unblocked next step
- verify after the step
- update plan or derived execution state when needed
- if implementation looks complete, run a stronger completion verification before returning `done`
- if verification still shows open gaps, do not return `done`; return `continue` or `stale_plan` instead
- do not perform close-out deletion
- return JSON only

Use these runner actions exactly:
- `continue` = another execution loop should run immediately
- `done` = implementation is complete and verification shows no material open execution gaps
- `blocked` = a real blocker prevents more execution
- `needs_user` = a user decision is required before continuing
- `stale_plan` = execution should stop and route through vico-plan before more implementation

Keep summaries concrete and brief. Mention exact verification evidence and the next recommended command when useful.
"""


def build_claude_command(args: argparse.Namespace, prompt: str) -> list[str]:
    command = [
        args.claude_command,
        "-p",
        "--output-format",
        "json",
        "--json-schema",
        json.dumps(RUNNER_SCHEMA, separators=(",", ":")),
        "--permission-mode",
        args.permission_mode,
        "--effort",
        args.effort,
    ]
    if args.model:
        command.extend(["--model", args.model])
    if args.bare:
        command.append("--bare")
    if args.dangerously_skip_permissions:
        command.append("--dangerously-skip-permissions")
    for directory in args.add_dir:
        command.extend(["--add-dir", directory])
    command.append(prompt)
    return command


def run_iteration(command: list[str], repo_root: Path) -> dict[str, str]:
    result = subprocess.run(command, cwd=repo_root, text=True, capture_output=True)
    if result.returncode != 0:
        raise SystemExit(
            f"Claude command failed with exit code {result.returncode}.\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    payload_text = result.stdout.strip()
    try:
        payload = json.loads(payload_text)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Claude runner expected JSON output but received:\n{payload_text}") from exc
    return payload


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    plan_path = resolve_active_plan(repo_root, args.slug)
    slug = plan_path.stem

    print(
        f"Vico Claude runner: repo={repo_root} slug={slug} max_iterations={args.max_iterations}",
        file=sys.stderr,
    )

    for iteration in range(1, args.max_iterations + 1):
        prompt = build_prompt(repo_root, plan_path)
        command = build_claude_command(args, prompt)
        payload = run_iteration(command, repo_root)

        print("", file=sys.stderr)
        print(f"=== Vico Claude Runner Iteration {iteration}/{args.max_iterations} ===", file=sys.stderr)
        print(f"action: {payload['runner_action']}", file=sys.stderr)
        print(f"summary: {payload['summary']}", file=sys.stderr)
        print(f"verification: {payload['verification']}", file=sys.stderr)
        print(f"next: {payload['next_step']}", file=sys.stderr)
        if payload["recommended_command"]:
            print(f"recommended_command: {payload['recommended_command']}", file=sys.stderr)

        action = payload["runner_action"]
        if action == "continue":
            continue
        if action == "done":
            return 0
        if action == "blocked":
            return 2
        if action == "needs_user":
            return 3
        if action == "stale_plan":
            return 4
        raise SystemExit(f"Unknown runner_action '{action}'")

    raise SystemExit(
        f"Runner reached max_iterations={args.max_iterations} without converging. Increase the limit or inspect the active plan."
    )


if __name__ == "__main__":
    raise SystemExit(main())
