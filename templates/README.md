# Templates

This directory contains copyable scaffolds for growing AgentConflictBench.

## Instance Template

Use `templates/instance/` when adding a benchmark instance. Copy it to
`instances/<instance_id>/`, then replace every placeholder before listing the
instance as `reproduced`.

Required follow-up:

1. Replace `patch_a.patch`, `patch_b.patch`, and `combined.patch` with
   apply-ready patch artifacts generated from the pinned base commit.
2. Replace the oracle files with language-appropriate tests.
3. Replace placeholder logs with captured validation logs:
   `validate_a.txt`, `validate_b.txt`, and `validate_composed.txt`.
4. Update `metadata.json` and `instances/index.json`.
5. Run:

```bash
python scripts/validate_metadata.py
python scripts/check_instance_completeness.py
python scripts/dataset_stats.py --output analysis/dataset_summary.md
python scripts/generate_dataset_table.py --output paper/dataset_table.md
```

The template is not itself a benchmark instance and is intentionally excluded
from dataset validation.
