#!/usr/bin/env bash
set -euo pipefail

python3 -m pytest "$(dirname "$0")/../oracle/test_composition.py" -q
