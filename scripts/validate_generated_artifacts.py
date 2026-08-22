#!/usr/bin/env python3
"""Regenerate generated artifacts and fail if they are stale."""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class GeneratedArtifact:
    path: str
    command: list[str]


ARTIFACTS = [
    GeneratedArtifact(
        "analysis/baseline_features.csv",
        [
            sys.executable,
            "scripts/baseline_features.py",
            "--output",
            "analysis/baseline_features.csv",
        ],
    ),
    GeneratedArtifact(
        "analysis/dataset_summary.md",
        [
            sys.executable,
            "scripts/dataset_stats.py",
            "--output",
            "analysis/dataset_summary.md",
        ],
    ),
    GeneratedArtifact(
        "paper/dataset_table.md",
        [
            sys.executable,
            "scripts/generate_dataset_table.py",
            "--output",
            "paper/dataset_table.md",
        ],
    ),
    GeneratedArtifact(
        "analysis/baseline_classifier_results.md",
        [
            sys.executable,
            "scripts/baseline_classifier.py",
            "--features",
            "analysis/baseline_features.csv",
            "--output",
            "analysis/baseline_classifier_results.md",
        ],
    ),
]


def run(cmd: list[str]) -> None:
    print(f"$ {' '.join(cmd)}", flush=True)
    subprocess.run(cmd, cwd=ROOT, check=True)


def main() -> int:
    for artifact in ARTIFACTS:
        run(artifact.command)

    paths = [artifact.path for artifact in ARTIFACTS]
    completed = subprocess.run(
        ["git", "diff", "--exit-code", "--", *paths],
        cwd=ROOT,
        text=True,
    )

    if completed.returncode != 0:
        print(
            "\nGenerated artifacts are stale. Run this command and commit the diff:\n"
            "\n  python scripts/validate_generated_artifacts.py\n"
        )
        return completed.returncode

    print("Generated artifact validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
