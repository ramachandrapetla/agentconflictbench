# Scripts

This directory contains setup, validation, composition, and benchmark-running scripts.

## Available scripts

- `run_instance.py`: validate one benchmark instance against a local upstream checkout.
- `bootstrap_repos.py`: clone upstream repositories referenced by the instance index.
- `dataset_stats.py`: generate Markdown dataset summary statistics from `instances/index.json`.
- `validate_metadata.py`: validate instance metadata, index consistency, enum values, and referenced files.
- `validate_dataset.py`: validate every reproduced instance listed in `instances/index.json` and write `analysis/validation_report.md`.

## Validate metadata

```bash
python scripts/validate_metadata.py
```

This check is intentionally dependency-free. It verifies that every
`instances/*/metadata.json` file follows `schema/metadata.schema.json`, that
`instances/index.json` agrees with the metadata files, and that patch, oracle,
and validation-script references point to existing files.

GitHub Actions runs this check automatically on pull requests and pushes to
`main`.

## Generate dataset summary

```bash
python scripts/dataset_stats.py --output analysis/dataset_summary.md
```

## Bootstrap upstream repositories

```bash
python scripts/bootstrap_repos.py --target-dir /tmp/agentconflictbench-repos --print-installs
```

This clones the upstream repositories referenced by `instances/index.json`.
Dependency installation remains explicit; see `../docs/reproduction.md`.

## Validate one instance

```bash
python scripts/run_instance.py instances/click__001 --repo-dir /tmp/click
```

## Validate the seed dataset

See `../docs/reproduction.md` for the current per-repository setup commands
and complete dataset-validation examples.

```bash
python scripts/validate_dataset.py \
  --repo click=/tmp/click \
  --repo typer=/tmp/typer
```

Use `--python` when different upstream repositories need different virtual environments:

```bash
python scripts/validate_dataset.py \
  --repo click=/tmp/click \
  --repo typer=/tmp/typer \
  --python click=/tmp/click/.venv/bin/python \
  --python typer=/tmp/typer/.venv/bin/python
```

A dataset validation pass means each included instance reproduces the expected AgentConflictBench pattern:

1. Patch A passes alone.
2. Patch B passes alone.
3. Patch A + Patch B applies cleanly.
4. The composition oracle fails as expected.

Python oracles are run with `pytest`. JavaScript oracles using `.js`, `.mjs`,
or `.cjs` are run with Node's built-in `node --test` runner. TypeScript
oracles using `.ts` or `.tsx` are run with a repo-local `tsx` loader.
