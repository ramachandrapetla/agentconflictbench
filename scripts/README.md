# Scripts

This directory contains setup, validation, composition, and benchmark-running scripts.

## Available scripts

- `run_instance.py`: validate one benchmark instance against a local upstream checkout.
- `bootstrap_repos.py`: clone upstream repositories referenced by the instance index.
- `baseline_features.py`: extract simple patch/task overlap features for baseline experiments.
- `baseline_classifier.py`: evaluate simple oracle-free conflict/control baselines over `analysis/baseline_features.csv`.
- `check_instance_completeness.py`: verify reproduced instances include the required tasks, patches, combined patch, oracles, scripts, logs, and docs.
- `dataset_stats.py`: generate Markdown dataset summary statistics from `instances/index.json`.
- `export_huggingface_dataset.py`: build a Hugging Face Dataset upload folder under `dist/huggingface/`.
- `generate_dataset_table.py`: generate a paper-facing instance table from `instances/index.json` and per-instance metadata.
- `validate_generated_artifacts.py`: regenerate generated CSV/Markdown artifacts and fail if they are stale.
- `validate_metadata.py`: validate instance metadata, index consistency, enum values, and referenced files.
- `validate_public_artifacts.py`: scan tracked files for local absolute paths and obvious credential-shaped strings before public release.
- `validate_dataset.py`: validate every reproduced instance listed in `instances/index.json` and write `analysis/validation_report.md`.

## Validate metadata

```bash
python scripts/validate_metadata.py
python scripts/check_instance_completeness.py
```

This check is intentionally dependency-free. It verifies that every
`instances/*/metadata.json` file follows `schema/metadata.schema.json`, that
`instances/index.json` agrees with the metadata files, and that patch, oracle,
and validation-script references point to existing files. The completeness
check additionally verifies the agreed instance shape for every reproduced
instance.

GitHub Actions runs this check automatically on pull requests and pushes to
`main`.

## Generate dataset summary

```bash
python scripts/dataset_stats.py --output analysis/dataset_summary.md
```

## Generate paper dataset table

```bash
python scripts/generate_dataset_table.py --output paper/dataset_table.md
```

This table is intended for paper drafting and reviewer-facing summaries. Keep
full per-instance detail in `../instances/` rather than expanding the root
README.

## Validate generated artifacts

```bash
python scripts/validate_generated_artifacts.py
```

This regenerates `analysis/baseline_features.csv`,
`analysis/dataset_summary.md`, `paper/dataset_table.md`, and
`analysis/baseline_classifier_results.md`, then fails if any of those generated
files differ from the committed versions.

## Validate public artifacts

```bash
python scripts/validate_public_artifacts.py
```

This checks tracked repository files for machine-specific absolute paths and
obvious credential-shaped strings. It is meant as a release/publication hygiene
guard, not as a replacement for manual review.

## Bootstrap upstream repositories

```bash
python scripts/bootstrap_repos.py --target-dir /tmp/agentconflictbench-repos --print-installs
```

This clones the upstream repositories referenced by `instances/index.json`.
Dependency installation remains explicit; see `../docs/reproduction.md`.

## Export for Hugging Face

```bash
python scripts/export_huggingface_dataset.py --output dist/huggingface
```

This creates a Hugging Face Dataset-ready folder with a dataset card,
`data/instances.jsonl`, `data/instances.csv`, and a zipped copy of the full
instance artifacts. See `../docs/huggingface.md`.

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
4. The composition oracle matches `composition_expected`.

Python oracles are run with `pytest`. JavaScript oracles using `.js`, `.mjs`,
or `.cjs` are run with Node's built-in `node --test` runner. TypeScript
oracles using `.ts` or `.tsx` are run with a repo-local `tsx` loader.
