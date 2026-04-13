#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


OWNER = Path("runtime") / "vico_artifacts" / "vico_common.py"
CLOSURES = [
    Path("vico-plan") / "scripts" / "vico_common.py",
    Path("vico-exec") / "scripts" / "vico_common.py",
]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sync shared Vico runtime owners into skill-local closure copies."
    )
    parser.add_argument(
        "--root",
        default=str(Path(__file__).resolve().parents[1]),
        help="vico-skills root directory",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Only check whether closures match the shared owner.",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    owner = root / OWNER
    if not owner.exists():
        raise SystemExit(f"Missing shared runtime owner: {owner}")

    owner_text = owner.read_text(encoding="utf-8")
    drifted: list[Path] = []
    for closure_rel in CLOSURES:
        closure = root / closure_rel
        if not closure.exists():
            raise SystemExit(f"Missing closure target: {closure}")
        closure_text = closure.read_text(encoding="utf-8")
        if closure_text == owner_text:
            print(f"Up to date: {closure}")
            continue
        drifted.append(closure)
        if args.check:
            print(f"Drifted: {closure}")
            continue
        closure.write_text(owner_text, encoding="utf-8")
        print(f"Synced: {closure}")

    if args.check and drifted:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
