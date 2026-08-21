#!/usr/bin/env bash
set -euo pipefail

# Run from the root of a pallets/click checkout after applying patch_a.diff and patch_b.diff.
# Expected outcome for this benchmark instance: pytest exits non-zero because
# Patch A + Patch B violates the composition oracle.
INSTANCE_DIR="${AGENTCONFLICT_INSTANCE_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"

python -m pytest "$INSTANCE_DIR/oracle/test_composition.py" -q
