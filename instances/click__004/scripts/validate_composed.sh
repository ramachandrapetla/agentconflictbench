#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="${1:?usage: validate_composed.sh /path/to/click}"
INSTANCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

git -C "$REPO_DIR" apply "$INSTANCE_DIR/patch_a.diff"
git -C "$REPO_DIR" apply "$INSTANCE_DIR/patch_b.diff"
python -m pytest "$INSTANCE_DIR/oracle/test_composition.py" -q
