#!/usr/bin/env python3
"""Clone upstream repositories used by AgentConflictBench instances.

The script prepares local checkouts only. It does not install dependencies by
default, because dependency installation can be slow and environment-specific.
Use ``--print-installs`` to show the current setup commands from the
reproduction guide.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]


INSTALL_NOTES = {
    "pallets/click": "python -m pip install -e . pytest",
    "fastapi/typer": "python -m pip install -e . pytest rich shellingham",
    "tj/commander.js": "no install required for current node:test oracles",
    "encode/httpx": "python -m pip install -e . pytest",
    "Textualize/rich": "python -m pip install -e . pytest",
    "colinhacks/zod": "npx pnpm@10.12.1 install --frozen-lockfile",
}


def repo_slug(repo: str) -> str:
    parsed = urlparse(repo)
    path = parsed.path.strip("/")
    if path.endswith(".git"):
        path = path[:-4]
    return path or repo


def checkout_name(slug: str) -> str:
    return slug.rsplit("/", 1)[-1]


def load_repositories(index_path: Path) -> dict[str, str]:
    data = json.loads(index_path.read_text())
    instances = data.get("instances", [])
    if not isinstance(instances, list):
        raise SystemExit(f"Invalid index format: {index_path}")

    repos: dict[str, str] = {}
    for instance in instances:
        if not isinstance(instance, dict):
            continue
        repo = instance.get("repo")
        if isinstance(repo, str):
            repos[repo_slug(repo)] = repo
    return dict(sorted(repos.items()))


def run(cmd: list[str], cwd: Path | None = None) -> None:
    print("$ " + " ".join(cmd), flush=True)
    subprocess.run(cmd, cwd=cwd, check=True)


def clone_repo(slug: str, url: str, target_root: Path, force: bool) -> Path:
    target = target_root / checkout_name(slug)

    if target.exists():
        if force:
            shutil.rmtree(target)
        else:
            print(f"skip existing: {target}")
            return target

    run(["git", "clone", url, str(target)])
    return target


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--index",
        type=Path,
        default=ROOT / "instances" / "index.json",
        help="Path to instances/index.json.",
    )
    parser.add_argument(
        "--target-dir",
        type=Path,
        default=Path("/tmp/agentconflictbench-repos"),
        help="Directory where upstream repositories should be cloned.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Delete and reclone existing target checkouts.",
    )
    parser.add_argument(
        "--print-installs",
        action="store_true",
        help="Print dependency installation notes after cloning.",
    )
    args = parser.parse_args()

    repos = load_repositories(args.index)
    args.target_dir.mkdir(parents=True, exist_ok=True)

    for slug, url in repos.items():
        target = clone_repo(slug, url, args.target_dir, args.force)
        if args.print_installs:
            note = INSTALL_NOTES.get(slug, "see docs/reproduction.md")
            print(f"# {slug}: cd {target} && {note}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
