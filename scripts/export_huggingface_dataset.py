#!/usr/bin/env python3
"""Export AgentConflictBench into a Hugging Face Dataset-ready folder."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
import zipfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_instances(index_path: Path) -> list[dict[str, Any]]:
    index = load_json(index_path)
    instances = index.get("instances", [])
    if not isinstance(instances, list):
        raise SystemExit(f"Invalid index format: {index_path}")
    return [instance for instance in instances if isinstance(instance, dict)]


def oracle_text(instance_dir: Path, relative_path: str) -> str:
    path = instance_dir / relative_path
    if path.is_file():
        return read_text(path)
    return ""


def find_oracle(instance_dir: Path, stem: str) -> str:
    matches = sorted((instance_dir / "oracle").glob(f"{stem}.*"))
    if not matches:
        return ""
    return str(matches[0].relative_to(instance_dir))


def build_rows(instances: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for instance in instances:
        instance_id = str(instance["id"])
        instance_dir = ROOT / str(instance["path"])
        metadata = load_json(instance_dir / "metadata.json")
        composition_oracle_path = str(metadata["composition_oracle"])
        patch_a_oracle_path = find_oracle(instance_dir, "test_patch_a")
        patch_b_oracle_path = find_oracle(instance_dir, "test_patch_b")

        rows.append(
            {
                "id": instance_id,
                "repo": metadata["repo"],
                "base_commit": metadata["base_commit"],
                "language": metadata["language"],
                "conflict_type": metadata["conflict_type"],
                "composition_expected": metadata["composition_expected"],
                "difficulty": metadata.get("difficulty", ""),
                "source": metadata["source"],
                "status": instance.get("status", ""),
                "task_a": read_text(instance_dir / "task_a.md"),
                "task_b": read_text(instance_dir / "task_b.md"),
                "task_a_summary": metadata["task_a"],
                "task_b_summary": metadata["task_b"],
                "patch_a": read_text(instance_dir / "patch_a.patch"),
                "patch_b": read_text(instance_dir / "patch_b.patch"),
                "combined_patch": read_text(instance_dir / "combined.patch"),
                "oracle_patch_a_path": patch_a_oracle_path,
                "oracle_patch_b_path": patch_b_oracle_path,
                "oracle_composition_path": composition_oracle_path,
                "oracle_patch_a": oracle_text(instance_dir, patch_a_oracle_path),
                "oracle_patch_b": oracle_text(instance_dir, patch_b_oracle_path),
                "oracle_composition": oracle_text(instance_dir, composition_oracle_path),
                "validation_a": metadata["validation_a"],
                "validation_b": metadata["validation_b"],
                "validation_composed": "scripts/validate_composed.sh",
                "merge_result": metadata["merge_result"],
                "failure_summary": metadata["failure_summary"],
                "notes": metadata.get("notes", ""),
                "github_instance_path": f"instances/{instance_id}",
            }
        )

    return rows


def write_jsonl(rows: list[dict[str, Any]], path: Path) -> None:
    with path.open("w", encoding="utf-8") as file:
        for row in rows:
            file.write(json.dumps(row, ensure_ascii=False) + "\n")


def write_csv(rows: list[dict[str, Any]], path: Path) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def zip_instances(path: Path) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for source in sorted((ROOT / "instances").rglob("*")):
            if source.is_file():
                archive.write(source, source.relative_to(ROOT))


def render_card(rows: list[dict[str, Any]], repo_id: str) -> str:
    positives = sum(1 for row in rows if row["composition_expected"] == "fail")
    controls = sum(1 for row in rows if row["composition_expected"] == "pass")
    repositories = sorted({row["repo"] for row in rows})
    languages = sorted({row["language"] for row in rows})

    return f"""---
license: mit
pretty_name: AgentConflictBench
language:
- code
tags:
- code
- software-engineering
- benchmark
- llm-agents
- program-repair
- semantic-conflicts
- multi-agent-systems
- tabular
task_categories:
- text-classification
size_categories:
- n<1K
configs:
- config_name: default
  data_files:
  - split: train
    path: data/instances.jsonl
---

# AgentConflictBench

AgentConflictBench is a research benchmark for evaluating silent semantic
conflicts among independently valid AI-generated code changes.

Most coding-agent benchmarks ask whether an agent can solve one task in
isolation. AgentConflictBench asks whether two independently valid patches
still work when composed.

## Dataset Summary

- Instances: {len(rows)}
- Positive silent semantic conflicts: {positives}
- Clean-composition controls: {controls}
- Upstream repositories: {len(repositories)}
- Languages: {", ".join(languages)}

Each row contains the task descriptions, reference patches, combined patch,
oracles, metadata, and validation-script references for one benchmark instance.
The full canonical instance folders are also included in
`artifacts/instances.zip`.

## Loading

```python
from datasets import load_dataset

dataset = load_dataset("{repo_id}")
print(dataset["train"][0]["id"])
```

## Fields

Important fields include:

- `id`
- `repo`
- `base_commit`
- `language`
- `conflict_type`
- `composition_expected`
- `task_a`
- `task_b`
- `patch_a`
- `patch_b`
- `combined_patch`
- `oracle_composition`
- `failure_summary`

`composition_expected = "fail"` means the instance is a positive silent
semantic conflict. `composition_expected = "pass"` means the instance is a
clean-composition control.

## Source Repository

Development repository:
https://github.com/ramachandrapetla/agentconflictbench

Contribution guide:
https://github.com/ramachandrapetla/agentconflictbench/blob/main/CONTRIBUTING.md

## Limitations

This is an early research artifact. The current seed dataset is intentionally
small, has only a few controls, and prioritizes Python and JavaScript/TypeScript
repositories. Full reproduction requires checking out upstream repositories and
installing their dependencies.

## Citation

If you use this benchmark, please cite this dataset and the GitHub repository.
A formal paper citation will be added when available.
"""


def copy_if_exists(source: Path, destination: Path) -> None:
    if source.exists():
        shutil.copy2(source, destination)


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
        default=ROOT / "dist" / "huggingface",
        help="Output folder to populate for Hugging Face upload.",
    )
    parser.add_argument(
        "--repo-id",
        default="ramachandra1996/agentconflictbench",
        help="Hugging Face dataset repo id used in the generated dataset card.",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Remove the output folder before rebuilding it.",
    )
    args = parser.parse_args()

    output = args.output
    if args.clean and output.exists():
        shutil.rmtree(output)

    data_dir = output / "data"
    artifacts_dir = output / "artifacts"
    data_dir.mkdir(parents=True, exist_ok=True)
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    rows = build_rows(load_instances(args.index))
    write_jsonl(rows, data_dir / "instances.jsonl")
    write_csv(rows, data_dir / "instances.csv")
    zip_instances(artifacts_dir / "instances.zip")
    (output / "README.md").write_text(render_card(rows, args.repo_id), encoding="utf-8")
    copy_if_exists(ROOT / "LICENSE", output / "LICENSE")
    copy_if_exists(ROOT / "CITATION.cff", output / "CITATION.cff")

    print(f"Wrote Hugging Face dataset package to {output}")
    print(f"Rows: {len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
