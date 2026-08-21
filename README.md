# AgentConflictBench

AgentConflictBench is a research benchmark for evaluating **silent semantic conflicts** among independently valid AI-generated code changes.

The core problem: current coding-agent benchmarks usually evaluate whether an agent can solve one software task in isolation. In real development, multiple AI-generated patches may be produced concurrently. Each patch can pass validation alone, Git can merge them without textual conflicts, and the combined system can still be wrong.

AgentConflictBench studies this composition failure mode.

## Definition

We define **silent semantic patch interference** as a conflict between two or more code changes where:

1. Each change independently passes its intended tests or validation.
2. The changes merge without textual Git conflicts.
3. The combined program fails a behavioral, architectural, security, schema, API-contract, configuration, invariant, or performance expectation.

## Benchmark Instance Rule

An instance belongs in AgentConflictBench only if:

1. Patch A applies to the base commit and passes independently.
2. Patch B applies to the same base commit and passes independently.
3. Patch A + Patch B merge without textual Git conflict.
4. Patch A + Patch B fail a composition-level oracle.
5. The failure is attributable to interaction between the patches.

## Repository Status

This repository is an early research artifact. The initial goal is to build a small, reproducible benchmark before scaling.

Current seed dataset:

- 7 benchmark instances
- 3 upstream repositories: `pallets/click`, `fastapi/typer`, `tj/commander.js`
- 3 conflict categories: `configuration`, `behavioral`, `api_contract`
- 7 reproduced clean-merge semantic failures

Planned first milestone:

- 50 to 100 benchmark instances
- 5 to 10 open-source repositories
- Python and TypeScript first
- at least 5 semantic conflict categories
- reproducible scripts or containers for every instance

## Reproducing One Instance

Clone the relevant upstream project and install its local test dependencies.

For the Click seeds:

```bash
git clone https://github.com/pallets/click.git /tmp/click
cd /tmp/click
python -m pip install -e . pytest
```

Then run:

```bash
python scripts/run_instance.py instances/click__001 --repo-dir /tmp/click
python scripts/run_instance.py instances/click__002 --repo-dir /tmp/click
python scripts/run_instance.py instances/click__003 --repo-dir /tmp/click
python scripts/run_instance.py instances/click__004 --repo-dir /tmp/click
```

For the Typer seed:

```bash
git clone https://github.com/fastapi/typer.git /tmp/typer
cd /tmp/typer
python -m pip install -e . pytest rich shellingham
```

Then run:

```bash
python scripts/run_instance.py instances/typer__001 --repo-dir /tmp/typer
python scripts/run_instance.py instances/typer__002 --repo-dir /tmp/typer
```

For the Commander seed:

```bash
git clone https://github.com/tj/commander.js.git /tmp/commander
cd /tmp/commander
```

Then run:

```bash
python scripts/run_instance.py instances/commander__001 --repo-dir /tmp/commander
```

A successful benchmark reproduction means Patch A passes alone, Patch B passes alone, and the composed oracle fails as expected.

## Validating The Dataset

Use `scripts/validate_dataset.py` to run every reproduced instance listed in `instances/index.json` and write a compact Markdown report.

If the upstream projects share the same Python environment:

```bash
python scripts/validate_dataset.py \
  --repo click=/tmp/click \
  --repo typer=/tmp/typer \
  --repo commander.js=/tmp/commander
```

If each upstream checkout has its own virtual environment, pass the Python executable for each repo:

```bash
python scripts/validate_dataset.py \
  --repo click=/tmp/click \
  --repo typer=/tmp/typer \
  --repo commander.js=/tmp/commander \
  --python click=/tmp/click/.venv/bin/python \
  --python typer=/tmp/typer/.venv/bin/python
```

Repository keys may be the repo name (`click`), owner/name (`pallets/click`), or full GitHub URL.

## Validating Metadata

Run the dependency-free metadata checker before adding or modifying benchmark
instances:

```bash
python scripts/validate_metadata.py
```

This verifies instance metadata, index consistency, enum values, commit SHA
format, and referenced patch/oracle/script files.

The same metadata and script-syntax checks run in GitHub Actions on pull
requests and pushes to `main`.

## Structure

```text
paper/       Research brief, methodology, and related work notes
instances/   Benchmark instances and metadata
schema/      Metadata schema for benchmark instances
scripts/     Reproduction and validation scripts
analysis/    Evaluation notebooks and result summaries
docs/        Roadmap and project documentation
```

## Citation

A formal citation will be added as the benchmark and paper mature. For now, see `CITATION.cff`.

## License

This repository is released under the MIT License unless otherwise noted. Individual benchmark instances may reference upstream repositories with their own licenses.
