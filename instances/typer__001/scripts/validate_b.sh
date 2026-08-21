#!/usr/bin/env bash
set -euo pipefail

# Run from the root of a fastapi/typer checkout after applying patch_b.patch.
INSTANCE_DIR="${AGENTCONFLICT_INSTANCE_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"

python -m pytest "$INSTANCE_DIR/oracle/test_patch_b.py" tests/test_core.py::test_group_click_resolve_command -q
