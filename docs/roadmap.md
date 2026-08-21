# Roadmap

## Milestone 1: Research Scaffold

- Define silent semantic patch interference.
- Publish research brief and methodology.
- Define benchmark metadata schema.
- Identify first candidate repositories.

## Milestone 2: Seeded Micro-Benchmark

- Build 10 to 20 controlled benchmark instances. The repository currently has
  15 reproduced instances.
- Cover at least 5 conflict categories.
- Package each instance with patches, scripts, logs, and oracle.
- Validate instance reproducibility.

## Current Near-Term Priorities

- Add the first `test_assumption` instance.
- Expand TypeScript coverage beyond one Zod seed.
- Grow from 15 to 20 reproduced instances while keeping the root README clean.
- Add at least one additional upstream repository before or during the next
  five-instance expansion.
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
