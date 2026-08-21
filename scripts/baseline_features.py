#!/usr/bin/env python3
"""Extract simple baseline features for AgentConflictBench instances."""

from __future__ import annotations

import argparse
import csv
import json
import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
TOKEN_RE = re.compile(r"[A-Za-z0-9_]+")


@dataclass(frozen=True)
class PatchFeatures:
    files: set[str]
    added_lines: int
    deleted_lines: int
    changed_tokens: set[str]


def repo_slug(repo: str) -> str:
    parsed = urlparse(repo)
    path = parsed.path.strip("/")
    if path.endswith(".git"):
        path = path[:-4]
    return path or repo


def load_index(index_path: Path) -> list[dict[str, object]]:
    data = json.loads(index_path.read_text())
    instances = data.get("instances", [])
    if not isinstance(instances, list):
        raise SystemExit(f"Invalid index format: {index_path}")
    return [instance for instance in instances if isinstance(instance, dict)]


def tokenize(text: str) -> set[str]:
    return {token.lower() for token in TOKEN_RE.findall(text)}


def jaccard(left: set[str], right: set[str]) -> float:
    if not left and not right:
        return 1.0
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def parse_patch(path: Path) -> PatchFeatures:
    files: set[str] = set()
    added_lines = 0
    deleted_lines = 0
    changed_tokens: set[str] = set()

    for line in path.read_text().splitlines():
        if line.startswith("diff --git "):
            parts = line.split()
            if len(parts) >= 4:
                files.add(parts[3].removeprefix("b/"))
            continue

        if line.startswith(("+++", "---")):
            continue

        if line.startswith("+"):
            added_lines += 1
            changed_tokens.update(tokenize(line[1:]))
        elif line.startswith("-"):
            deleted_lines += 1
            changed_tokens.update(tokenize(line[1:]))

    return PatchFeatures(
        files=files,
        added_lines=added_lines,
        deleted_lines=deleted_lines,
        changed_tokens=changed_tokens,
    )


def render_rows(root: Path, instances: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    for instance in instances:
        instance_id = str(instance.get("id", ""))
        instance_dir = root / "instances" / instance_id
        metadata = json.loads((instance_dir / "metadata.json").read_text())

        patch_a = parse_patch(instance_dir / "patch_a.patch")
        patch_b = parse_patch(instance_dir / "patch_b.patch")
        task_a_tokens = tokenize((instance_dir / "task_a.md").read_text())
        task_b_tokens = tokenize((instance_dir / "task_b.md").read_text())
        shared_files = patch_a.files & patch_b.files

        rows.append(
            {
                "id": instance_id,
                "repo": repo_slug(str(instance.get("repo", ""))),
                "language": instance.get("language", ""),
                "conflict_type": instance.get("conflict_type", ""),
                "difficulty": metadata.get("difficulty", ""),
                "patch_a_files": len(patch_a.files),
                "patch_b_files": len(patch_b.files),
                "shared_files": len(shared_files),
                "same_file": int(bool(shared_files)),
                "both_single_file": int(len(patch_a.files) == 1 and len(patch_b.files) == 1),
                "patch_a_added_lines": patch_a.added_lines,
                "patch_a_deleted_lines": patch_a.deleted_lines,
                "patch_b_added_lines": patch_b.added_lines,
                "patch_b_deleted_lines": patch_b.deleted_lines,
                "changed_token_jaccard": f"{jaccard(patch_a.changed_tokens, patch_b.changed_tokens):.4f}",
                "task_token_jaccard": f"{jaccard(task_a_tokens, task_b_tokens):.4f}",
            }
        )

    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--index",
        type=Path,
        default=ROOT / "instances" / "index.json",
        help="Path to instances/index.json.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "analysis" / "baseline_features.csv",
        help="CSV output path.",
    )
    args = parser.parse_args()

    rows = render_rows(ROOT, load_index(args.index))
    args.output.parent.mkdir(parents=True, exist_ok=True)

    with args.output.open("w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
