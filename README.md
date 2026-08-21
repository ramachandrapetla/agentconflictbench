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

- 4 benchmark instances
- 2 upstream repositories: `pallets/click`, `fastapi/typer`
- 3 conflict categories: `configuration`, `behavioral`, `api_contract`
- 4 reproduced clean-merge semantic failures

Planned first milestone:

- 50 to 100 benchmark instances
- 5 to 10 open-source repositories
- Python and TypeScript first
- at least 5 semantic conflict categories
- reproducible scripts or containers for every instance

## Reproducing An Instance

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
```

A successful benchmark reproduction means Patch A passes alone, Patch B passes alone, and the composed oracle fails as expected.

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
