# AgentConflictBench

[![Validate](https://github.com/ramachandrapetla/agentconflictbench/actions/workflows/validate.yml/badge.svg)](https://github.com/ramachandrapetla/agentconflictbench/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Dataset: 28 instances](https://img.shields.io/badge/dataset-28%20instances-blue)](analysis/dataset_summary.md)

AgentConflictBench is a research benchmark for evaluating **silent semantic conflicts** among independently valid AI-generated code changes.

The core problem: current coding-agent benchmarks usually evaluate whether an agent can solve one software task in isolation. In real development, multiple AI-generated patches may be produced concurrently. Each patch can pass validation alone, Git can merge them without textual conflicts, and the combined system can still be wrong.

AgentConflictBench studies this composition failure mode.

In one sentence: **SWE-bench asks whether an agent can solve one task; AgentConflictBench asks whether independently valid agent patches still work when composed.**

## Definition

We define **silent semantic patch interference** as a conflict between two or more code changes where:

1. Each change independently passes its intended tests or validation.
2. The changes merge without textual Git conflicts.
3. The combined program fails a behavioral, architectural, security, schema, API-contract, configuration, invariant, or performance expectation.

## Benchmark Instance Rule

AgentConflictBench includes positive conflict instances and clean-composition
controls. A positive conflict instance belongs in the benchmark only if:

1. Patch A applies to the base commit and passes independently.
2. Patch B applies to the same base commit and passes independently.
3. Patch A + Patch B merge without textual Git conflict.
4. Patch A + Patch B fail a composition-level oracle.
5. The failure is attributable to interaction between the patches.

A control instance follows the same structure, but its composed oracle is
expected to pass. Controls are labeled with `composition_expected = "pass"` and
`conflict_type = "control"`.

## Repository Status

This repository is an early research artifact. The initial goal is to build a small, reproducible benchmark before scaling.

Current seed dataset:

- 28 reproduced benchmark instances
- 25 positive conflict instances and 3 clean-composition controls
- 7 upstream repositories: `pallets/click`, `fastapi/typer`, `tj/commander.js`, `encode/httpx`, `pallets/markupsafe`, `Textualize/rich`, `colinhacks/zod`
- 7 categories: `configuration`, `behavioral`, `api_contract`, `security_policy`, `state_invariant`, `test_assumption`, `control`
- 25 reproduced clean-merge semantic failures

Planned first milestone:

- 50 to 100 benchmark instances
- 5 to 10 open-source repositories
- Python and TypeScript first
- at least 5 semantic conflict categories
- reproducible scripts or containers for every instance

## Reproduction

Each benchmark instance is reproduced against a pinned upstream commit. A
successful reproduction means Patch A passes alone, Patch B passes alone, the
patches apply together without textual conflict, and the composed oracle matches
the instance's `composition_expected` label.

After setting up the relevant upstream checkout:

```bash
python scripts/run_instance.py instances/click__001 --repo-dir /tmp/click
```

For upstream setup commands, per-repository dependency notes, and full-dataset
validation examples, see [docs/reproduction.md](docs/reproduction.md).

For a short walkthrough of one benchmark instance, see [docs/demo.md](docs/demo.md).
For a quick artifact review path, see
[docs/artifact_review_checklist.md](docs/artifact_review_checklist.md).

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
templates/   Copyable scaffolds for new benchmark instances
```

## Contributing

Contributions are welcome. The easiest places to help are:

- add a new clean-composition control instance;
- add a new positive conflict instance from an already-supported repository;
- improve reproduction tooling;
- add baseline detectors or analysis scripts;
- improve the paper notes and related-work coverage.

Start with [CONTRIBUTING.md](CONTRIBUTING.md) and
[docs/contributor_instance_guide.md](docs/contributor_instance_guide.md). Good
first issues are tracked in GitHub Issues.

If you want to share the project, [`docs/launch_post.md`](docs/launch_post.md)
has a short public summary you can adapt.

## Citation

A formal citation will be added as the benchmark and paper mature. For now, see `CITATION.cff`.

## License

This repository is released under the MIT License unless otherwise noted. Individual benchmark instances may reference upstream repositories with their own licenses.
