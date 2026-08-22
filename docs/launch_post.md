# Public Launch Draft

Use this as a starting point for LinkedIn, GitHub Discussions, email outreach,
or a project announcement. Edit the tone before posting.

## Short Version

I’m building AgentConflictBench, a benchmark for silent semantic conflicts in
concurrent AI-generated code changes.

Most coding-agent benchmarks ask whether an agent can solve one task in
isolation. AgentConflictBench asks a different question: if two independently
valid agent patches both pass their own tests and merge cleanly, does the
combined program still behave correctly?

The current public seed dataset has 28 reproduced instances across 7
open-source repositories: 25 positive conflict instances and 3 clean-composition
controls. Each instance includes task descriptions, reference patches,
composition patches, oracles, validation scripts, logs, and metadata.

Repo: https://github.com/ramachandrapetla/agentconflictbench

I’d love feedback, collaborators, and new benchmark instances—especially clean
controls, dependency conflicts, performance/resource conflicts, and baseline
evaluators.

## Slightly Longer Version

I made AgentConflictBench public:

https://github.com/ramachandrapetla/agentconflictbench

The core idea is simple:

- Patch A passes independently.
- Patch B passes independently.
- Git applies A+B without textual conflict.
- The composed behavior can still be wrong.

This is the gap AgentConflictBench targets. As AI coding agents become more
common, teams will increasingly have multiple independently generated changes
landing near each other. Traditional merge conflict detection and isolated
task-level tests do not fully cover that interaction surface.

The repo currently includes:

- 28 reproduced benchmark instances;
- 25 positive silent semantic conflicts;
- 3 clean-composition controls;
- 7 upstream repositories;
- canonical task/patch/oracle/script/log metadata for each instance;
- validation tooling and generated paper-facing dataset summaries.

The positioning I’m exploring is:

> SWE-bench asks whether an agent can solve one task. AgentConflictBench asks
> whether independently valid agent patches still work when composed.

I’m looking for collaborators interested in software engineering benchmarks,
LLM coding agents, semantic merge conflicts, program repair, testing, and
multi-agent coding workflows.

Good first contributions:

- add more clean-composition controls;
- add dependency or performance/resource conflict instances;
- improve Docker/reproduction support;
- implement simple baseline classifiers;
- strengthen related work and paper framing.

Contributing guide:

https://github.com/ramachandrapetla/agentconflictbench/blob/main/CONTRIBUTING.md

Demo:

https://github.com/ramachandrapetla/agentconflictbench/blob/main/docs/demo.md

## One-Line Pitch

AgentConflictBench evaluates whether independently valid AI-generated patches
still work when composed.
