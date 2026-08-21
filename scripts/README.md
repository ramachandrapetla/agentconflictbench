# Scripts

This directory contains setup, validation, composition, and benchmark-running scripts.

## Available scripts

- `run_instance.py`: validate one benchmark instance against a local upstream checkout.
- `validate_dataset.py`: validate every reproduced instance listed in `instances/index.json` and write `analysis/validation_report.md`.

## Validate one instance

```bash
python scripts/run_instance.py instances/click__001 --repo-dir /tmp/click
```

## Validate the seed dataset

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
