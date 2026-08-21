#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="${1:?usage: validate_a.sh /path/to/httpx}"
INSTANCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

git -C "$REPO_DIR" apply "$INSTANCE_DIR/patch_a.diff"
python -m pytest "$INSTANCE_DIR/oracle/test_patch_a.py" -q
