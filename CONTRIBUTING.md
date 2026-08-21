# Contributing to AgentConflictBench

Thank you for considering a contribution. AgentConflictBench is an early
research benchmark, so careful, reproducible contributions matter more than raw
volume.

## Good First Contributions

The best starting points are:

- add a clean-composition control instance;
- improve documentation for reproducing existing instances;
- add a baseline detector or analysis script;
- propose a candidate upstream repository;
- improve paper notes, related work, or taxonomy documentation.

## Instance Contributions

New instances must follow the canonical layout documented in
[`instances/README.md`](instances/README.md):

```text
task_a.md
task_b.md
patch_a.patch
patch_b.patch
combined.patch
oracle/
scripts/
logs/
metadata.json
README.md
```

Positive conflict instances should have:

- Patch A passes alone.
- Patch B passes alone.
- Patch A + Patch B applies cleanly.
- The composition oracle fails.
- `composition_expected` is `"fail"`.

Control instances should have:

- Patch A passes alone.
- Patch B passes alone.
- Patch A + Patch B applies cleanly.
- The composition oracle passes.
- `composition_expected` is `"pass"`.
- `conflict_type` is `"control"`.

See [`docs/contributor_instance_guide.md`](docs/contributor_instance_guide.md)
for the full checklist.

## Validation

Before opening a pull request, run:

```bash
python scripts/validate_metadata.py
python scripts/check_instance_completeness.py
python scripts/validate_generated_artifacts.py
python scripts/validate_public_artifacts.py
```

If you add or modify an instance, also run:

```bash
python scripts/run_instance.py instances/<instance_id> --repo-dir /path/to/upstream
```

For a full dataset run, see [`docs/reproduction.md`](docs/reproduction.md).

## Pull Request Expectations

Please include:

- a short summary of the change;
- which instance or docs are affected;
- validation commands and results;
- any setup caveats for upstream dependencies.

Avoid committing local virtual environments, package caches, build outputs, or
machine-specific absolute paths.
