# Benchmark Instances

This directory will contain AgentConflictBench instances.

Each accepted instance should include:

- metadata.json
- task_a.md
- task_b.md
- patch_a.diff
- patch_b.diff
- oracle/
- scripts/
- logs/
- README.md

An instance is accepted only when both patches pass independently, merge without textual Git conflict, and fail a composition-level oracle when combined.
