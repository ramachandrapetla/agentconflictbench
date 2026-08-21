#!/usr/bin/env python3
"""Scan tracked files for content that should not be published.

The scanner is intentionally conservative and narrow. It catches local absolute
paths and common credential-shaped strings while avoiding broad words such as
``token`` or ``secret`` that appear legitimately in benchmark examples.
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Finding:
    path: Path
    line_number: int
    label: str


PATTERNS = [
    ("local user path", re.compile(r"/Users/[A-Za-z0-9._-]+/")),
    ("temporary checkout path", re.compile(r"/private/tmp/[A-Za-z0-9._/-]+")),
    ("Codex workspace path", re.compile(r"Documents/Codex")),
    ("OpenAI API key", re.compile(r"sk-[A-Za-z0-9_-]{20,}")),
    ("GitHub classic token", re.compile(r"ghp_[A-Za-z0-9_]{20,}")),
    ("GitHub fine-grained token", re.compile(r"github_pat_[A-Za-z0-9_]{20,}")),
    ("AWS access key", re.compile(r"AKIA[0-9A-Z]{16}")),
    (
        "private key block",
        re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC |DSA |)PRIVATE KEY-----"),
    ),
]


def tracked_files() -> list[Path]:
    completed = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    return [ROOT / line for line in completed.stdout.splitlines() if line]


def scan_file(path: Path) -> list[Finding]:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return []

    findings: list[Finding] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        for label, pattern in PATTERNS:
            if pattern.search(line):
                findings.append(Finding(path, line_number, label))
    return findings


def main() -> int:
    findings: list[Finding] = []
    for path in tracked_files():
        if path.relative_to(ROOT) == Path("scripts/validate_public_artifacts.py"):
            continue
        findings.extend(scan_file(path))

    if findings:
        print("Public artifact validation failed:")
        for finding in findings:
            relative = finding.path.relative_to(ROOT)
            print(f"- {relative}:{finding.line_number}: {finding.label}")
        return 1

    print("Public artifact validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
