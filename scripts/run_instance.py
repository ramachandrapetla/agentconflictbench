#!/usr/bin/env python3
"""Run an AgentConflictBench instance against a local repository checkout."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CheckoutState:
    """The branch/commit state to restore after an instance run."""

    commit: str
    branch: str | None


def run(
    cmd: list[str],
    cwd: Path,
    expect_failure: bool = False,
    env: dict[str, str] | None = None,
) -> int:
    print(f"$ {' '.join(cmd)}", flush=True)
    completed = subprocess.run(cmd, cwd=cwd, text=True, env=env)

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


def get_checkout_state(repo_dir: Path) -> CheckoutState:
    """Capture the current commit and branch, if HEAD is attached."""
    commit = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=repo_dir, text=True
    ).strip()
    branch_result = subprocess.run(
        ["git", "symbolic-ref", "--quiet", "--short", "HEAD"],
        cwd=repo_dir,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    branch = branch_result.stdout.strip() if branch_result.returncode == 0 else None
    return CheckoutState(commit=commit, branch=branch)


def reset_repo(repo_dir: Path) -> None:
    """Discard changes made by a benchmark phase while preserving ignored deps."""
    run(["git", "reset", "--hard", "HEAD"], cwd=repo_dir)
    run(["git", "clean", "-fd"], cwd=repo_dir)


def checkout_base(repo_dir: Path, base_commit: str) -> None:
    run(["git", "checkout", "--detach", base_commit], cwd=repo_dir)


def restore_checkout(repo_dir: Path, state: CheckoutState) -> None:
    """Return a clean repository to the branch/commit it started on."""
    reset_repo(repo_dir)
    if state.branch is not None:
        run(["git", "switch", state.branch], cwd=repo_dir)
    else:
        checkout_base(repo_dir, state.commit)


def apply_patch(repo_dir: Path, patch_path: Path) -> None:
    run(["git", "apply", str(patch_path)], cwd=repo_dir)


def run_oracle(repo_dir: Path, test_path: str, expect_failure: bool = False) -> None:
    suffix = Path(test_path).suffix

    if suffix == ".py":
        cmd = [sys.executable, "-m", "pytest", test_path, "-q"]
        env = None
        src_dir = repo_dir / "src"
        if src_dir.is_dir():
            env = os.environ.copy()
            existing_pythonpath = env.get("PYTHONPATH")
            env["PYTHONPATH"] = (
                str(src_dir)
                if not existing_pythonpath
                else f"{src_dir}{os.pathsep}{existing_pythonpath}"
            )
        run(cmd, cwd=repo_dir, expect_failure=expect_failure, env=env)
        return
    elif suffix in {".js", ".mjs", ".cjs"}:
        cmd = ["node", "--test", test_path]
    elif suffix in {".ts", ".tsx"}:
        tsx_loader = repo_dir / "node_modules" / "tsx" / "dist" / "loader.mjs"
        if not tsx_loader.exists():
            raise SystemExit(
                "TypeScript oracles require a repo-local tsx install at "
                f"{tsx_loader}"
            )
        cmd = [
            "node",
            "--import",
            str(tsx_loader),
            "--conditions",
            "@zod/source",
            test_path,
        ]
    else:
        raise SystemExit(f"Unsupported oracle file extension: {test_path}")

    run(cmd, cwd=repo_dir, expect_failure=expect_failure)


def find_oracle(instance_dir: Path, stem: str) -> Path:
    matches = sorted((instance_dir / "oracle").glob(f"{stem}.*"))

    if not matches:
        raise SystemExit(f"Missing oracle file: oracle/{stem}.*")

    if len(matches) > 1:
        names = ", ".join(str(path) for path in matches)
        raise SystemExit(f"Ambiguous oracle files for {stem}: {names}")

    return matches[0]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Reproduce an AgentConflictBench instance against a local upstream checkout."
    )
    parser.add_argument("instance_dir", type=Path)
    parser.add_argument("--repo-dir", type=Path, required=True)
    parser.add_argument(
        "--skip-clean-check",
        action="store_true",
        help=(
            "Skip checking that the repository checkout is clean before running. "
            "Warning: benchmark cleanup discards tracked and untracked changes."
        ),
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

    original_checkout = get_checkout_state(repo_dir)
    base_commit = metadata["base_commit"]
    patch_a = instance_dir / metadata["patch_a"]
    patch_b = instance_dir / metadata["patch_b"]

    patch_a_test = str(find_oracle(instance_dir, "test_patch_a"))
    patch_b_test = str(find_oracle(instance_dir, "test_patch_b"))
    composition_test = str(instance_dir / "oracle" / "test_composition.py")
    if "composition_oracle" in metadata:
        composition_test = str(instance_dir / metadata["composition_oracle"])
    composition_expected = metadata["composition_expected"]
    if composition_expected not in {"fail", "pass"}:
        raise SystemExit(
            "metadata field composition_expected must be one of: fail, pass"
        )

    try:
        print(f"Running {metadata['id']} against {repo_dir}")

        checkout_base(repo_dir, base_commit)

        print("\n[1/3] Patch A validation")
        apply_patch(repo_dir, patch_a)
        run_oracle(repo_dir, patch_a_test)
        reset_repo(repo_dir)

        print("\n[2/3] Patch B validation")
        apply_patch(repo_dir, patch_b)
        run_oracle(repo_dir, patch_b_test)
        reset_repo(repo_dir)

        print("\n[3/3] Composition validation")
        apply_patch(repo_dir, patch_a)
        apply_patch(repo_dir, patch_b)
        run_oracle(
            repo_dir,
            composition_test,
            expect_failure=composition_expected == "fail",
        )

        if composition_expected == "fail":
            print("\nPASS: instance reproduces expected silent semantic conflict.")
        else:
            print("\nPASS: instance reproduces expected clean composition control.")
        return 0
    finally:
        restore_checkout(repo_dir, original_checkout)


if __name__ == "__main__":
    raise SystemExit(main())
