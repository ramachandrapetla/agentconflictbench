#!/usr/bin/env bash
set -euo pipefail

# Run from the root of a pallets/click checkout after applying patch_a.diff.
INSTANCE_DIR="${AGENTCONFLICT_INSTANCE_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"

python -m pytest "$INSTANCE_DIR/oracle/test_patch_a.py" tests/test_defaults.py::test_default_map_source -q
