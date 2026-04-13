#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


AGENT_SECTION_RE = re.compile(
    r"^## Agent Summary\s*$([\s\S]*?)(?=^## |\Z)", re.MULTILINE
)
FIELD_RE = re.compile(
    r"^- `(?P<label>Display name|Short description|Default prompt)`: `(?P<value>.*)`\s*$",
    re.MULTILINE,
)


def find_skill_dirs(root: Path) -> list[Path]:
    return sorted(
        path for path in root.iterdir() if path.is_dir() and (path / "SKILL.md").exists()
    )


def parse_agent_summary(skill_md: Path) -> dict[str, str]:
    text = skill_md.read_text(encoding="utf-8")
    match = AGENT_SECTION_RE.search(text)
    if not match:
        raise SystemExit(f"Missing `## Agent Summary` in {skill_md}")

    values: dict[str, str] = {}
    for field_match in FIELD_RE.finditer(match.group(1)):
        values[field_match.group("label")] = field_match.group("value")

    required = ["Display name", "Short description", "Default prompt"]
    missing = [label for label in required if label not in values]
    if missing:
        raise SystemExit(f"Missing agent summary field(s) {missing} in {skill_md}")
    return values


def render_openai_yaml(summary: dict[str, str]) -> str:
    return (
        "interface:\n"
        f"  display_name: {json.dumps(summary['Display name'])}\n"
        f"  short_description: {json.dumps(summary['Short description'])}\n"
        f"  default_prompt: {json.dumps(summary['Default prompt'])}\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sync agents/openai.yaml from skill-local Agent Summary blocks."
    )
    parser.add_argument(
        "--root",
        default=str(Path(__file__).resolve().parents[1]),
        help="vico-skills root directory",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Only check whether generated files are up to date.",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    drifted = False
    for skill_dir in find_skill_dirs(root):
        summary = parse_agent_summary(skill_dir / "SKILL.md")
        rendered = render_openai_yaml(summary)
        target = skill_dir / "agents" / "openai.yaml"
        current = target.read_text(encoding="utf-8") if target.exists() else None
        if current == rendered:
            print(f"Up to date: {target}")
            continue
        drifted = True
        if args.check:
            print(f"Drifted: {target}")
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(rendered, encoding="utf-8")
        print(f"Wrote {target}")

    if args.check and drifted:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
