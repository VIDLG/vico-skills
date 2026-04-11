#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
META_LINE_RE = re.compile(r"^\s*>?\s*([A-Za-z][A-Za-z ]*[A-Za-z]):\s*(.*?)\s*$")
META_START_RE = re.compile(
    r"^\s*>?\s*(Status|Mode|Progress|Slug|Manifest|Created|Updated|Completed|Source PRD|Execution Plan|Related plan|Current architecture|Superseded by):\s*"
)
PATHISH_KEYS = {
    "manifest",
    "source_prd",
    "execution_plan",
    "related_plan",
    "current_architecture",
    "superseded_by",
}
PREFERRED_META_ORDER = [
    "status",
    "mode",
    "progress",
    "slug",
    "manifest",
    "created",
    "updated",
    "completed",
    "source_prd",
    "execution_plan",
    "related_plan",
    "current_architecture",
    "superseded_by",
]
PROGRESS_ALIASES = {
    "near_complete": "mostly_complete",
    "partial": "partially_completed",
}
RELATIONSHIP_KEYS = {
    "related",
    "follow_up",
    "supersedes",
    "superseded_by",
}


@dataclass
class MetadataBlock:
    start: int
    end: int
    blockquote: bool
    entries: list[tuple[str, str, str]]


def normalize_key(label: str) -> str:
    return label.strip().lower().replace(" ", "_")


def clean_value(raw_value: str) -> str:
    value = raw_value.strip()
    if value.startswith("`") and value.endswith("`") and len(value) >= 2:
        return value[1:-1]
    return value


def today_iso() -> str:
    return date.today().isoformat()


def repo_root_from_arg(repo_root: str | None) -> Path:
    root = Path(repo_root).resolve() if repo_root else Path.cwd().resolve()
    vico_dir = root / ".vico"
    if not vico_dir.exists():
        raise SystemExit(f"Missing .vico workspace under {root}")
    return root


def read_json(path: Path) -> dict | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str, *, overwrite: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not overwrite:
        raise FileExistsError(f"Refusing to overwrite existing file: {path}")
    path.write_text(text, encoding="utf-8")


def relative_path(root: Path, target: Path) -> str:
    return target.resolve().relative_to(root).as_posix()


def index_path(root: Path, slug: str) -> Path:
    return root / ".vico" / "index" / f"{slug}.json"


def plan_path(root: Path, slug: str) -> Path:
    return root / ".vico" / "plans" / "active" / f"{slug}.md"


def prd_path(root: Path, slug: str) -> Path:
    return root / ".vico" / "prd" / "active" / f"{slug}.md"


def resume_path(root: Path, slug: str) -> Path:
    return root / ".vico" / "resume" / f"{slug}.md"


def architecture_doc_path(root: Path, slug: str) -> Path:
    return root / "docs" / "architecture" / f"{slug}.md"


def detect_metadata(path: Path, line_limit: int = 40) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    metadata: dict[str, str] = {}
    for line in lines[:line_limit]:
        match = META_LINE_RE.match(line)
        if not match:
            continue
        metadata[normalize_key(match.group(1))] = clean_value(match.group(2))
    return metadata


def find_metadata_block(text: str, line_limit: int = 40) -> MetadataBlock:
    lines = text.splitlines(keepends=True)
    start = None
    for index, line in enumerate(lines[:line_limit]):
        if META_START_RE.match(line):
            start = index
            break
    if start is None:
        raise ValueError("Could not find top metadata block")

    end = start
    while end < len(lines):
        stripped = lines[end].rstrip("\n")
        if end > start and stripped == "":
            break
        if META_START_RE.match(lines[end]):
            end += 1
            continue
        if end == start:
            end += 1
            continue
        break

    entries: list[tuple[str, str, str]] = []
    for line in lines[start:end]:
        match = META_LINE_RE.match(line.rstrip("\n"))
        if not match:
            continue
        label = match.group(1).strip()
        value = clean_value(match.group(2))
        entries.append((normalize_key(label), label, value))

    return MetadataBlock(
        start=start,
        end=end,
        blockquote=lines[start].lstrip().startswith(">"),
        entries=entries,
    )


def format_metadata_line(label: str, value: str, blockquote: bool) -> str:
    prefix = "> " if blockquote else ""
    wrap = blockquote or normalize_key(label) in PATHISH_KEYS
    rendered = f"`{value}`" if wrap else value
    return f"{prefix}{label}: {rendered}\n"


def update_metadata_text(text: str, updates: dict[str, tuple[str, str | None]]) -> str:
    lines = text.splitlines(keepends=True)
    block = find_metadata_block(text)

    values: dict[str, tuple[str, str]] = {}
    original_order: list[str] = []
    for norm_key, label, value in block.entries:
        values[norm_key] = (label, value)
        original_order.append(norm_key)

    for norm_key, (label, value) in updates.items():
        if value is None:
            values.pop(norm_key, None)
            continue
        values[norm_key] = (label, value)
        if norm_key not in original_order:
            original_order.append(norm_key)

    ordered_keys: list[str] = []
    for norm_key in PREFERRED_META_ORDER:
        if norm_key in values:
            ordered_keys.append(norm_key)
    for norm_key in original_order:
        if norm_key in values and norm_key not in ordered_keys:
            ordered_keys.append(norm_key)

    replacement = [
        format_metadata_line(values[norm_key][0], values[norm_key][1], block.blockquote)
        for norm_key in ordered_keys
    ]
    new_lines = lines[: block.start] + replacement + lines[block.end :]
    return "".join(new_lines)


def active_slugs(root: Path) -> set[str]:
    slugs: set[str] = set()
    for directory in (
        root / ".vico" / "plans" / "active",
        root / ".vico" / "prd" / "active",
        root / ".vico" / "resume",
        root / ".vico" / "index",
    ):
        if not directory.exists():
            continue
        for path in directory.iterdir():
            if path.name == "README.md":
                continue
            if path.suffix not in {".md", ".json"}:
                continue
            slugs.add(path.stem)
    return slugs


def architecture_paths(root: Path, slug: str, existing_index: dict | None) -> list[str]:
    found: list[str] = []
    default_arch = root / "docs" / "architecture" / f"{slug}.md"
    if default_arch.exists():
        found.append(relative_path(root, default_arch))

    if existing_index:
        for raw_path in existing_index.get("artifacts", {}).get("architecture", []):
            path = root / Path(raw_path)
            if path.exists():
                rel = relative_path(root, path)
                if rel not in found:
                    found.append(rel)
    return found


def derive_progress(status: str, existing_progress: str | None = None) -> str:
    if existing_progress:
        return PROGRESS_ALIASES.get(existing_progress, existing_progress)
    normalized = status.strip().lower()
    if normalized in {"done", "completed", "archived"}:
        return "done"
    if normalized in {"partial", "partially_completed"}:
        return "partial"
    if normalized in {"accepted", "not_started"}:
        return "not_started"
    return "partial"


def normalize_relationships(existing_index: dict | None) -> dict[str, list[str]]:
    if not existing_index:
        return {}
    raw_relationships = existing_index.get("relationships", {})
    if not isinstance(raw_relationships, dict):
        return {}

    relationships: dict[str, list[str]] = {}
    for key, value in raw_relationships.items():
        if key not in RELATIONSHIP_KEYS or not isinstance(value, list):
            continue
        cleaned = [item for item in value if isinstance(item, str) and item.strip()]
        if cleaned:
            relationships[key] = cleaned
    return relationships


def build_index_manifest(root: Path, slug: str, existing_index: dict | None) -> dict | None:
    plan = plan_path(root, slug)
    prd = prd_path(root, slug)
    resume = resume_path(root, slug)

    if not plan.exists() and not prd.exists() and not resume.exists():
        return None

    plan_meta = detect_metadata(plan) if plan.exists() else {}
    prd_meta = detect_metadata(prd) if prd.exists() else {}
    existing_state = existing_index.get("state", {}) if existing_index else {}

    status = plan_meta.get("status") or existing_state.get("status") or prd_meta.get("status") or "in_progress"
    progress = plan_meta.get("progress") or derive_progress(status, existing_state.get("progress"))
    tracking_mode = (
        plan_meta.get("mode")
        or prd_meta.get("mode")
        or existing_state.get("tracking_mode")
        or ("prd_backed" if prd.exists() else "plan_only")
    )
    updated = plan_meta.get("updated") or prd_meta.get("updated") or existing_state.get("updated") or today_iso()

    artifacts: dict[str, object] = {}
    if prd.exists():
        artifacts["prd"] = relative_path(root, prd)
    if plan.exists():
        artifacts["plan"] = relative_path(root, plan)
    if resume.exists():
        artifacts["resume_current"] = relative_path(root, resume)

    arch_paths = architecture_paths(root, slug, existing_index)
    if arch_paths:
        artifacts["architecture"] = arch_paths

    relationships = normalize_relationships(existing_index)

    manifest = {
        "kind": "vico-linkage-v1",
        "slug": slug,
        "state": {
            "status": status,
            "progress": progress,
            "tracking_mode": tracking_mode,
            "updated": updated,
        },
        "artifacts": artifacts,
    }
    if relationships:
        manifest["relationships"] = relationships
    return manifest


def ensure_vico_layout(root: Path) -> None:
    required_dirs = [
        root / ".vico" / "index",
        root / ".vico" / "plans" / "active",
        root / ".vico" / "prd" / "active",
        root / ".vico" / "resume",
    ]
    for directory in required_dirs:
        directory.mkdir(parents=True, exist_ok=True)


def sync_active_headers_for_slug(root: Path, slug: str, *, touch_updated: bool = False, current_date: str | None = None) -> list[Path]:
    current_date = current_date or today_iso()
    changed: list[Path] = []
    manifest = index_path(root, slug)
    manifest_rel = relative_path(root, manifest) if manifest.exists() else None
    plan = plan_path(root, slug)
    prd = prd_path(root, slug)

    if plan.exists():
        plan_meta = detect_metadata(plan)
        plan_updates: dict[str, tuple[str, str | None]] = {
            "slug": ("Slug", slug),
            "mode": ("Mode", "prd_backed" if prd.exists() else "plan_only"),
            "manifest": ("Manifest", manifest_rel),
            "source_prd": ("Source PRD", relative_path(root, prd) if prd.exists() else None),
            "created": ("Created", plan_meta.get("created") or current_date),
            "updated": ("Updated", current_date if touch_updated else (plan_meta.get("updated") or current_date)),
        }
        updated_text = update_metadata_text(plan.read_text(encoding="utf-8"), plan_updates)
        if updated_text != plan.read_text(encoding="utf-8"):
            plan.write_text(updated_text, encoding="utf-8")
            changed.append(plan)

    if prd.exists():
        prd_meta = detect_metadata(prd)
        prd_updates: dict[str, tuple[str, str | None]] = {
            "slug": ("Slug", slug),
            "mode": ("Mode", "prd_backed"),
            "manifest": ("Manifest", manifest_rel),
            "execution_plan": ("Execution Plan", relative_path(root, plan) if plan.exists() else None),
            "created": ("Created", prd_meta.get("created") or current_date),
            "updated": ("Updated", current_date if touch_updated else (prd_meta.get("updated") or current_date)),
        }
        updated_text = update_metadata_text(prd.read_text(encoding="utf-8"), prd_updates)
        if updated_text != prd.read_text(encoding="utf-8"):
            prd.write_text(updated_text, encoding="utf-8")
            changed.append(prd)

    return changed
