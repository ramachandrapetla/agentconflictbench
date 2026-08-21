#!/usr/bin/env python3
"""Run an AgentConflictBench instance against a local repository checkout."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], cwd: Path, expect_failure: bool = False) -> int:
    print(f"$ {' '.join(cmd)}", flush=True)
    completed = subprocess.run(cmd, cwd=cwd, text=True)

    if expect_failure:
        if completed.returncode == 0:
            raise SystemExit("Expected command to fail, but it succeeded.")
    elif completed.returncode != 0:
        raise SystemExit(completed.returncode)

    return completed.returncode


def require_clean_repo(repo_dir: Path) -> None:
    status = subprocess.check_output(
        ["git", "status", "--short"], cwd=repo_dir, text=True
    ).strip()

    if status:
        raise SystemExit(
            f"Repository checkout is not clean: {repo_dir}\n"
            "Use a fresh clone or clean the checkout before running an instance."
        )


def restore_repo(repo_dir: Path) -> None:
    run(["git", "restore", "."], cwd=repo_dir)


def checkout_base(repo_dir: Path, base_commit: str) -> None:
    run(["git", "checkout", "--detach", base_commit], cwd=repo_dir)


def apply_patch(repo_dir: Path, patch_path: Path) -> None:
    run(["git", "apply", str(patch_path)], cwd=repo_dir)


def run_pytest(repo_dir: Path, tests: list[str], expect_failure: bool = False) -> None:
    run([sys.executable, "-m", "pytest", *tests, "-q"], cwd=repo_dir, expect_failure=expect_failure)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Reproduce an AgentConflictBench instance against a local upstream checkout."
    )
    parser.add_argument("instance_dir", type=Path)
    parser.add_argument("--repo-dir", type=Path, required=True)
    parser.add_argument(
        "--skip-clean-check",
        action="store_true",
        help="Skip checking that the repository checkout is clean before running.",
    )
    args = parser.parse_args()

    instance_dir = args.instance_dir.resolve()
    repo_dir = args.repo_dir.resolve()
    metadata = json.loads((instance_dir / "metadata.json").read_text())

    if not (repo_dir / ".git").exists():
        raise SystemExit(f"Not a Git checkout: {repo_dir}")

    if not shutil.which("git"):
        raise SystemExit("git is required.")

    if not args.skip_clean_check:
        require_clean_repo(repo_dir)

    base_commit = metadata["base_commit"]
    patch_a = instance_dir / metadata["patch_a"]
    patch_b = instance_dir / metadata["patch_b"]

    patch_a_test = str(instance_dir / "oracle" / "test_patch_a.py")
    patch_b_test = str(instance_dir / "oracle" / "test_patch_b.py")
    composition_test = str(instance_dir / "oracle" / "test_composition.py")

    try:
        print(f"Running {metadata['id']} against {repo_dir}")

        checkout_base(repo_dir, base_commit)

        print("\n[1/3] Patch A validation")
        apply_patch(repo_dir, patch_a)
        run_pytest(repo_dir, [patch_a_test])
        restore_repo(repo_dir)

        print("\n[2/3] Patch B validation")
        apply_patch(repo_dir, patch_b)
        run_pytest(repo_dir, [patch_b_test])
        restore_repo(repo_dir)

        print("\n[3/3] Composition validation")
        apply_patch(repo_dir, patch_a)
        apply_patch(repo_dir, patch_b)
        run_pytest(repo_dir, [composition_test], expect_failure=True)

        print("\nPASS: instance reproduces expected silent semantic conflict.")
        return 0
    finally:
        restore_repo(repo_dir)


if __name__ == "__main__":
    raise SystemExit(main())
