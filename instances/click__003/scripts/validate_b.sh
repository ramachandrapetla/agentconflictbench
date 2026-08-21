#!/usr/bin/env bash
set -euo pipefail

# Run from the root of a pallets/click checkout after applying patch_b.diff.
INSTANCE_DIR="${AGENTCONFLICT_INSTANCE_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"

python -m pytest "$INSTANCE_DIR/oracle/test_patch_b.py" tests/test_commands.py::test_group_add_command_name -q
