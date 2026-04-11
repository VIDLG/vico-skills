#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from vico_common import detect_metadata, index_path, plan_path, prd_path, relative_path, repo_root_from_arg, resume_path


DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ACTIVE_PLAN_STATUSES = {"in_progress", "accepted", "draft"}
ACTIVE_PRD_STATUSES = {"accepted", "in_progress", "draft"}
PROGRESS_VALUES = {"not_started", "partially_completed", "mostly_complete", "done"}
ALIGNMENT_VALUES = {"aligned", "partially_aligned", "diverged"}
WORK_STATUS_VALUES = {"done", "partial", "not_started", "diverged", "unclear"}
CONFIDENCE_VALUES = {"high", "medium", "low"}
RELATIONSHIP_KEYS = {"related", "follow_up", "supersedes", "superseded_by"}
TRACKING_MODE_VALUES = {"plan_only", "prd_backed"}


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def is_iso_date(value: str | None) -> bool:
    return bool(value and DATE_RE.match(value))


def validate_plan(path: Path, root: Path, errors: list[str]) -> None:
    meta = detect_metadata(path)
    require(meta.get("slug") == path.stem, f"{path}: slug must match filename", errors)
    require(meta.get("status") in ACTIVE_PLAN_STATUSES, f"{path}: invalid active plan status {meta.get('status')!r}", errors)
    require(meta.get("mode") in TRACKING_MODE_VALUES, f"{path}: invalid Mode {meta.get('mode')!r}", errors)
    require(is_iso_date(meta.get("created")), f"{path}: Created must be YYYY-MM-DD", errors)
    require(is_iso_date(meta.get("updated")), f"{path}: Updated must be YYYY-MM-DD", errors)
    if "progress" in meta:
        require(meta["progress"] in PROGRESS_VALUES, f"{path}: invalid Progress {meta['progress']!r}", errors)
    manifest = meta.get("manifest")
    if manifest:
        require((root / manifest).exists(), f"{path}: Manifest path does not exist: {manifest}", errors)
    source_prd = meta.get("source_prd")
    if source_prd:
        require((root / source_prd).exists(), f"{path}: Source PRD path does not exist: {source_prd}", errors)


def validate_prd(path: Path, root: Path, errors: list[str]) -> None:
    meta = detect_metadata(path)
    require(meta.get("slug") == path.stem, f"{path}: slug must match filename", errors)
    require(meta.get("status") in ACTIVE_PRD_STATUSES, f"{path}: invalid active PRD status {meta.get('status')!r}", errors)
    require(meta.get("mode") == "prd_backed", f"{path}: PRD Mode must be 'prd_backed'", errors)
    require(is_iso_date(meta.get("created")), f"{path}: Created must be YYYY-MM-DD", errors)
    require(is_iso_date(meta.get("updated")), f"{path}: Updated must be YYYY-MM-DD", errors)
    manifest = meta.get("manifest")
    if manifest:
        require((root / manifest).exists(), f"{path}: Manifest path does not exist: {manifest}", errors)
    execution_plan = meta.get("execution_plan") or meta.get("related_plan")
    if execution_plan:
        require((root / execution_plan).exists(), f"{path}: execution plan path does not exist: {execution_plan}", errors)


def validate_resume(path: Path, root: Path, errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    required_sections = [
        "## Resume Summary",
        "## Verified Progress",
        "## Evidence",
        "## Divergences",
        "## Unresolved Areas",
        "## Recommended Next Step",
        "## Recommended Doc Updates",
    ]
    for section in required_sections:
        require(section in text, f"{path}: missing section {section}", errors)

    summary_values: dict[str, str] = {}
    in_summary = False
    for line in text.splitlines():
        if line.strip() == "## Resume Summary":
            in_summary = True
            continue
        if in_summary and line.startswith("## "):
            break
        if in_summary and line.startswith("- ") and ":" in line:
            label, value = line[2:].split(":", 1)
            summary_values[label.strip().lower()] = value.strip().strip("`")

    alignment = summary_values.get("alignment")
    if alignment:
        require(alignment in ALIGNMENT_VALUES, f"{path}: invalid Alignment {alignment!r}", errors)
    overall = summary_values.get("overall implementation status")
    if overall:
        require(overall in WORK_STATUS_VALUES, f"{path}: invalid overall implementation status {overall!r}", errors)
    confidence = summary_values.get("confidence")
    if confidence:
        require(confidence in CONFIDENCE_VALUES, f"{path}: invalid Confidence {confidence!r}", errors)
    manifest = summary_values.get("manifest")
    if manifest and manifest != "optional .vico/index/<slug>.json":
        require((root / manifest).exists(), f"{path}: referenced manifest does not exist: {manifest}", errors)


def validate_index(path: Path, root: Path, errors: list[str]) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    require(data.get("kind") == "vico-linkage-v1", f"{path}: kind must be vico-linkage-v1", errors)
    require(data.get("slug") == path.stem, f"{path}: slug must match filename", errors)
    state = data.get("state", {})
    require(state.get("status") in ACTIVE_PLAN_STATUSES, f"{path}: invalid state.status {state.get('status')!r}", errors)
    require(state.get("progress") in PROGRESS_VALUES, f"{path}: invalid state.progress {state.get('progress')!r}", errors)
    tracking_mode = state.get("tracking_mode")
    if tracking_mode is not None:
        require(tracking_mode in TRACKING_MODE_VALUES, f"{path}: invalid state.tracking_mode {tracking_mode!r}", errors)
    require(is_iso_date(state.get("updated")), f"{path}: state.updated must be YYYY-MM-DD", errors)
    artifacts = data.get("artifacts", {})
    allowed_keys = {"prd", "plan", "resume_current", "architecture"}
    for key in artifacts:
        require(key in allowed_keys, f"{path}: unexpected artifact key {key!r}", errors)
    for key in ("prd", "plan", "resume_current"):
        artifact = artifacts.get(key)
        if artifact:
            require((root / artifact).exists(), f"{path}: artifact path does not exist for {key}: {artifact}", errors)
    for artifact in artifacts.get("architecture", []):
        require((root / artifact).exists(), f"{path}: architecture path does not exist: {artifact}", errors)
    relationships = data.get("relationships", {})
    require(isinstance(relationships, dict), f"{path}: relationships must be an object when present", errors)
    if isinstance(relationships, dict):
        for key, value in relationships.items():
            require(key in RELATIONSHIP_KEYS, f"{path}: unexpected relationship key {key!r}", errors)
            require(isinstance(value, list), f"{path}: relationship {key!r} must be a list", errors)
            if isinstance(value, list):
                for related_slug in value:
                    require(isinstance(related_slug, str) and bool(related_slug.strip()), f"{path}: relationship {key!r} contains an invalid slug", errors)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the current .vico workspace against Vico document conventions.")
    parser.add_argument("--repo-root", help="Repository root. Defaults to the current working directory.")
    args = parser.parse_args()

    root = repo_root_from_arg(args.repo_root)
    errors: list[str] = []

    for path in sorted((root / ".vico" / "plans" / "active").glob("*.md")):
        if path.name != "README.md":
            validate_plan(path, root, errors)
    for path in sorted((root / ".vico" / "prd" / "active").glob("*.md")):
        if path.name != "README.md":
            validate_prd(path, root, errors)
    for path in sorted((root / ".vico" / "resume").glob("*.md")):
        if path.name != "README.md":
            validate_resume(path, root, errors)
    for path in sorted((root / ".vico" / "index").glob("*.json")):
        validate_index(path, root, errors)

    if errors:
        print("Vico workspace validation failed:\n")
        for error in errors:
            print(error)
        return 1

    print("Vico workspace validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
