#!/usr/bin/env python3
from __future__ import annotations

import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
# Owner source: runtime/cli/bootstrap_vico_slug.py
OWNER = ROOT / "runtime" / "cli" / "bootstrap_vico_slug.py"


if __name__ == "__main__":
    runpy.run_path(str(OWNER), run_name="__main__")
