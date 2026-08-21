#!/usr/bin/env python3
"""Validate every reproduced AgentConflictBench instance in an index.

The script is intentionally thin: it delegates the per-instance semantics to
``scripts/run_instance.py`` and adds dataset-level orchestration, repository
mapping, and a compact report.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class RunResult:
    instance_id: str
    repo: str
    status: str
    returncode: int
    output: str


def repo_aliases(repo: str) -> set[str]:
    """Return accepted aliases for a repository URL or slug."""

    parsed = urlparse(repo)
    path = parsed.path.strip("/")
    if path.endswith(".git"):
        path = path[:-4]

    aliases = {repo, path}
    if "/" in path:
        owner, name = path.rsplit("/", 1)
        aliases.update({name, f"{owner}/{name}"})

    return {alias for alias in aliases if alias}


def parse_mapping(values: list[str], flag: str) -> dict[str, str]:
    mapping: dict[str, str] = {}

    for value in values:
        if "=" not in value:
            raise SystemExit(f"{flag} entries must use KEY=VALUE syntax: {value}")

        key, mapped_value = value.split("=", 1)
        key = key.strip()
        mapped_value = mapped_value.strip()

        if not key or not mapped_value:
            raise SystemExit(f"{flag} entries must include both KEY and VALUE: {value}")

        mapping[key] = mapped_value

    return mapping


def resolve_mapping(repo: str, mapping: dict[str, str], label: str) -> str:
    aliases = repo_aliases(repo)

    for alias in aliases:
        if alias in mapping:
            return mapping[alias]

    expected = ", ".join(sorted(aliases))
    raise SystemExit(
        f"No {label} mapping found for {repo}. "
        f"Provide one of these aliases: {expected}"
    )


def run_instance(
    runner: Path,
    instance_dir: Path,
    repo_dir: Path,
    python_executable: str,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            python_executable,
            str(runner),
            str(instance_dir),
            "--repo-dir",
            str(repo_dir),
        ],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )


def resolve_executable(value: str) -> str:
    """Make path-like executable values absolute without dereferencing venv symlinks."""

    if os.sep in value or (os.altsep and os.altsep in value):
        path = Path(value)
        if not path.is_absolute():
            path = Path.cwd() / path

        return str(path.absolute())

    return value


def render_report(results: list[RunResult]) -> str:
    generated_at = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    passed = sum(result.status == "pass" for result in results)
    failed = len(results) - passed

    lines = [
        "# Dataset Validation Report",
        "",
        f"Generated: `{generated_at}`",
        "",
        f"Validated instances: {len(results)}",
        f"Passed reproductions: {passed}",
        f"Failed reproductions: {failed}",
        "",
        "| Instance | Repository | Status |",
        "|---|---|---:|",
    ]

    for result in results:
        marker = "PASS" if result.status == "pass" else "FAIL"
        lines.append(f"| `{result.instance_id}` | `{result.repo}` | {marker} |")

    lines.extend(
        [
            "",
        "A PASS means Patch A passed alone, Patch B passed alone, and the "
        "A+B composition oracle matched the instance's composition_expected value.",
        "",
        ]
    )

    if failed:
        lines.append("## Failed outputs")
        lines.append("")

        for result in results:
            if result.status == "pass":
                continue

            lines.extend(
                [
                    f"### {result.instance_id}",
                    "",
                    "```text",
                    result.output.rstrip(),
                    "```",
                    "",
                ]
            )

    return "\n".join(lines)


def load_instances(index_path: Path, statuses: set[str]) -> list[dict[str, object]]:
    data = json.loads(index_path.read_text())
    instances = data.get("instances", [])

    if not isinstance(instances, list):
        raise SystemExit(f"Invalid index format: {index_path}")

    selected: list[dict[str, object]] = []
    for instance in instances:
        if not isinstance(instance, dict):
            raise SystemExit(f"Invalid instance entry in {index_path}: {instance!r}")

        if str(instance.get("status", "")) in statuses:
            selected.append(instance)

    return selected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--index",
        type=Path,
        default=ROOT / "instances" / "index.json",
        help="Path to the dataset index.",
    )
    parser.add_argument(
        "--repo",
        action="append",
        default=[],
        metavar="KEY=PATH",
        help=(
            "Map an upstream repository to a local checkout. KEY can be a full "
            "URL, owner/name, or repo name. Repeat for each upstream repo."
        ),
    )
    parser.add_argument(
        "--python",
        action="append",
        default=[],
        metavar="KEY=PATH",
        help=(
            "Optional Python executable per upstream repo. KEY follows --repo. "
            "Defaults to the Python running this script."
        ),
    )
    parser.add_argument(
        "--status",
        action="append",
        default=["reproduced"],
        help="Instance status to include. Defaults to reproduced.",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=ROOT / "analysis" / "validation_report.md",
        help="Markdown report path.",
    )
    args = parser.parse_args()

    repo_map = parse_mapping(args.repo, "--repo")
    python_map = parse_mapping(args.python, "--python")
    statuses = set(args.status)
    runner = ROOT / "scripts" / "run_instance.py"

    if not runner.exists():
        raise SystemExit(f"Missing runner: {runner}")

    instances = load_instances(args.index, statuses)
    if not instances:
        raise SystemExit(f"No instances found with statuses: {', '.join(sorted(statuses))}")

    results: list[RunResult] = []

    for instance in instances:
        instance_id = str(instance["id"])
        repo = str(instance["repo"])
        instance_dir = ROOT / str(instance["path"])
        repo_dir = Path(resolve_mapping(repo, repo_map, "repository")).resolve()
        python_executable = sys.executable

        for alias in repo_aliases(repo):
            if alias in python_map:
                python_executable = resolve_executable(python_map[alias])
                break

        print(f"==> {instance_id} ({repo})", flush=True)
        completed = run_instance(runner, instance_dir, repo_dir, python_executable)
        status = "pass" if completed.returncode == 0 else "fail"
        results.append(
            RunResult(
                instance_id=instance_id,
                repo=repo,
                status=status,
                returncode=completed.returncode,
                output=completed.stdout,
            )
        )

        print(f"    {status.upper()}", flush=True)

    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(render_report(results))
    print(f"\nWrote report: {args.report}")

    return 0 if all(result.status == "pass" for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
