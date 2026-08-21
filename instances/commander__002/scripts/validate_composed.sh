#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="${1:?usage: validate_composed.sh /path/to/commander.js}"
INSTANCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

git -C "$REPO_DIR" apply "$INSTANCE_DIR/patch_a.diff"
git -C "$REPO_DIR" apply "$INSTANCE_DIR/patch_b.diff"
cd "$REPO_DIR"
node --test "$INSTANCE_DIR/oracle/test_composition.mjs"
