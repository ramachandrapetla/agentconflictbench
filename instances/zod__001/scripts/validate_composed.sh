#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="${1:?usage: validate_composed.sh /path/to/zod}"
INSTANCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

git -C "$REPO_DIR" apply "$INSTANCE_DIR/patch_a.diff"
git -C "$REPO_DIR" apply "$INSTANCE_DIR/patch_b.diff"
cd "$REPO_DIR"
node --import ./node_modules/tsx/dist/loader.mjs --conditions @zod/source "$INSTANCE_DIR/oracle/test_composition.ts"
