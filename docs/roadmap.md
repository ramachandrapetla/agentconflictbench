# Roadmap

## Milestone 1: Research Scaffold

- Define silent semantic patch interference.
- Publish research brief and methodology.
- Define benchmark metadata schema.
- Identify first candidate repositories.

## Milestone 2: Seeded Micro-Benchmark

- Build 25 to 30 controlled benchmark instances. The repository currently has
  28 reproduced instances: 25 positive conflicts and 3 controls.
- Cover at least 5 conflict categories. The current seed dataset covers 7,
  including the `control` category for clean-composition examples.
- Package each instance with patches, scripts, logs, and oracle.
- Validate instance reproducibility.

## Current Near-Term Priorities

- Grow clean-composition controls from 3 to at least 10.
- Expand beyond supported repositories with one carefully selected additional
  JavaScript/TypeScript repository.
- Add dependency and performance/resource examples.
- Begin running baseline feature analysis over every new dataset snapshot.
- Maintain a near-duplicate rejection record for every new accepted instance.

## Milestone 3: Real Repository Benchmark

- Expand to 50 to 100 instances.
- Use 5 to 10 open-source repositories.
- Focus initially on Python and TypeScript.
- Add Docker or scripted reproduction support.

## Milestone 4: Baseline Evaluation

- Evaluate textual overlap baselines.
- Evaluate patch-size baselines.
- Evaluate test-suite and static-analysis baselines.
- Evaluate agent-review baselines.
- Prototype lightweight risk prediction.

## Milestone 5: Paper Submission

- Complete related work.
- Report dataset construction methodology.
- Report taxonomy and benchmark statistics.
- Report baseline results.
- Release artifact and archived dataset version.
