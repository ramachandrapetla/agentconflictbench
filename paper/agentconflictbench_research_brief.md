# AgentConflictBench Research Brief

## Working Title

**AgentConflictBench: A Benchmark for Silent Semantic Conflicts in Concurrent AI-Generated Code Changes**

## Working Abstract

AI coding agents are increasingly used to implement software changes, but current evaluations largely measure whether an agent can solve an individual task in isolation. As these agents become part of parallel development workflows, correctness can no longer be evaluated only at the level of a single patch. Two independently valid patches may each pass their intended tests, merge cleanly in Git, and still produce a combined system that violates expected behavior.

This project introduces **silent semantic patch interference**, a failure mode in which independently correct AI-generated code changes compose into an incorrect program without producing a textual merge conflict. AgentConflictBench is a benchmark for measuring, classifying, and detecting these failures in concurrent AI-assisted software development.

The benchmark consists of paired software-development tasks where each patch is valid in isolation, the combined patches merge without textual conflicts, and the merged system fails behavioral, API-contract, invariant, security, schema, configuration, architectural, or performance expectations.

## Core Claim

Current coding-agent benchmarks evaluate whether AI agents can solve individual software engineering tasks, but they do not systematically evaluate what happens when multiple independently correct AI-generated patches are combined.

AgentConflictBench asks whether independently solved tasks remain correct when their generated patches are composed.

## Novelty Wedge

Existing work evaluates individual coding-agent task completion, agent-team coordination, textual merge conflicts, semantic merge-conflict detection, and AI-generated code quality. However, there is no widely established benchmark focused on silent semantic interference among independently valid AI-generated patches that merge cleanly but fail when composed.

The contribution is the intersection of:

1. AI-generated patches.
2. Independent validity of each patch.
3. Clean textual merge.
4. Composition-level semantic failure.
5. Benchmark format with taxonomy, oracles, and detection baselines.

## Research Questions

**RQ1. How often do independently valid AI-generated patches interfere when composed?**

Measure the composition failure rate: the percentage of cleanly merged patch pairs that fail the composition-level oracle.

**RQ2. What types of semantic interference occur in concurrent AI-generated code changes?**

Classify failures into a taxonomy of behavioral, API-contract, invariant, schema, configuration, security-policy, performance, test-assumption, and architectural conflicts.

**RQ3. Can existing validation mechanisms detect these conflicts before merge?**

Evaluate repository tests, task-specific tests, generated tests, static analysis, type checks, code review heuristics, and agent self-review.

**RQ4. Can lightweight predictors identify high-risk patch pairs?**

Study features from diffs, touched files, dependency graphs, test coverage, call graphs, and natural-language task descriptions.

## Expected Contributions

1. A formal definition of silent semantic patch interference in AI-generated software changes.
2. A benchmark of paired coding-agent tasks where individually valid patches compose into invalid merged systems.
3. A taxonomy of semantic conflict types specific to concurrent AI-assisted development.
4. Baseline evaluations for conflict detection using tests, static analysis, agent review, and lightweight risk prediction.

## Key Related Areas

- Coding-agent benchmarks such as SWE-bench.
- Multi-agent coding benchmarks such as CooperBench.
- AI-agent textual merge-conflict datasets such as AgenticFlict.
- LLM merge-conflict resolution benchmarks such as Merge-Bench.
- Semantic merge-conflict detection research.
- AI-generated code quality and maintainability studies.
