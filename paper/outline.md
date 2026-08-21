# AgentConflictBench Paper Outline

## Working Title

AgentConflictBench: Evaluating Silent Semantic Conflicts in Concurrent
AI-Generated Code Changes

## Abstract Sketch

AI coding agents are increasingly able to solve individual software tasks, but
real development workflows compose multiple changes. Two independently valid
agent-generated patches may each pass their local tests, merge without textual
conflict, and still produce an incorrect combined program. We introduce silent
semantic patch interference, a failure mode for concurrent AI-assisted
development, and present AgentConflictBench, a benchmark of paired coding tasks
that expose these composition failures. The benchmark packages pinned upstream
commits, independently valid patch pairs, clean textual merges, and
composition-level oracles. We report a taxonomy of conflict types and evaluate
baseline detection methods ranging from textual overlap to test-based and
agent-review approaches.

## 1. Introduction

- Coding-agent evaluation currently emphasizes isolated task success.
- Concurrent agent workflows create a second-order correctness problem:
  individually valid patches may not compose.
- Textual merge success is not semantic success.
- AgentConflictBench targets this gap with reproducible paired-task instances.

## 2. Problem Definition

Define silent semantic patch interference as a patch pair where:

1. both patches start from the same base commit;
2. each patch passes its own validation oracle;
3. the patches merge without textual conflict;
4. the composed program fails a composition-level oracle;
5. the failure is attributable to the interaction between patches.

## 3. Benchmark Construction

- Repository selection criteria.
- Task-pair generation and researcher construction.
- Patch packaging format.
- Oracle design.
- Quality checklist and rejection criteria.
- Reproduction scripts and metadata schema.

## 4. Dataset

Current seed benchmark:

- 10 reproduced instances.
- 5 upstream repositories.
- 3 languages.
- 3 conflict categories.

Planned submission benchmark:

- 50 to 100 reproduced instances.
- 5 to 10 upstream repositories.
- at least 5 conflict categories.
- Python and TypeScript/JavaScript first.

## 5. Taxonomy

Initial categories:

- behavioral
- API contract
- configuration

Planned categories:

- security policy
- test assumption
- dependency
- state invariant
- performance/resource
- architectural
- database schema

## 6. Baseline Experiments

Evaluate whether the following detect or predict composition failure:

- textual overlap;
- same-file overlap;
- touched-symbol overlap;
- patch size and changed-file counts;
- task-description similarity;
- repository test suite;
- generated composition tests;
- static/type checks;
- coding-agent review prompts.

## 7. Metrics

- composition failure detection precision/recall;
- false-positive rate on clean compositions;
- per-category detection rate;
- validation cost;
- oracle execution time;
- explanation quality for review-based baselines.

## 8. Threats To Validity

- researcher-constructed instances may overrepresent cleanly explainable
  failures;
- seed repositories may bias toward libraries with compact local tests;
- local oracles may miss larger integration consequences;
- generated patches may differ from future coding-agent behavior;
- dependency setup may affect reproducibility.

## 9. Artifact

- public GitHub repository;
- pinned metadata for each instance;
- patch files and oracles;
- validation scripts;
- generated dataset summary;
- archived release for submission.

## 10. Expected Contributions

1. Formalization of silent semantic patch interference.
2. A reproducible benchmark of clean-merge semantic conflicts.
3. A taxonomy of conflict types for concurrent AI-generated patches.
4. Baseline results for detecting risky patch compositions.
5. An artifact suitable for extension by the research community.
