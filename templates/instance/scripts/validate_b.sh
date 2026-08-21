#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="${1:?usage: validate_b.sh /path/to/upstream/repo}"
INSTANCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

git -C "$REPO_DIR" apply "$INSTANCE_DIR/patch_b.patch"
cd "$REPO_DIR"
python -m pytest "$INSTANCE_DIR/oracle/test_patch_b.py" -q
