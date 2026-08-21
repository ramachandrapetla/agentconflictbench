# Benchmark Methodology

AgentConflictBench uses a hybrid construction strategy. Pure mining may miss silent semantic failures because they do not appear as Git conflicts. Pure manual construction risks looking artificial. The benchmark therefore combines mined, agent-generated, and researcher-constructed task pairs.

## Construction Pipeline

1. Select repositories.
2. Generate or identify independent task pairs.
3. Produce candidate patches from the same base commit.
4. Validate each patch independently.
5. Compose patch pairs and detect clean-merge failures.
6. Label, audit, and package accepted instances.

## Instance Packaging

Each accepted instance is packaged as a pair of standalone task intents and a
pair of apply-ready reference implementations:

- `task_a.md` and `task_b.md` describe the independent development intents.
- `patch_a.patch` and `patch_b.patch` are the reference implementations for
  those intents.
- `combined.patch` records the clean textual composition of both patches.
- `oracle/test_patch_a.*`, `oracle/test_patch_b.*`, and
  `oracle/test_composition.*` encode the independent and composed acceptance
  conditions.

This separates what an agent is asked to do from the golden patch artifact used
for benchmark reproduction. The distinction makes the dataset usable both as a
patch-composition benchmark and as future task-level agent evaluation input.

## Inclusion Criteria

Each instance must satisfy:

1. Both tasks start from the same base commit.
2. Each task has a plausible standalone software-development goal.
3. Patch A applies cleanly and passes independently.
4. Patch B applies cleanly and passes independently.
5. Patch A + Patch B merge without textual Git conflict.
6. The composed program fails at least one composition-level oracle.
7. The failure is attributable to interaction between the patches.
8. The instance is reproducible from pinned commands and metadata.

## Exclusion Criteria

Exclude an instance when either patch fails independently, Git reports a textual conflict, the failure is caused by setup or flakiness, the composition failure cannot be reproduced, or the task pair is not realistic.

Also exclude or hold candidates that are near-duplicates of accepted instances:
same repository subsystem, same hidden contract, same conflict type, and same
oracle shape. These candidates are useful during exploration, but counting them
as separate benchmark items would overstate dataset diversity.

Rejected or held candidates are recorded in `docs/rejected_candidates.md`.
This creates an audit trail for negative selection decisions and makes the
benchmark construction process more reviewable.

## Composition Oracle

A composition-level oracle may be a unit test, integration test, property-based test, regression test, static policy check, controlled performance threshold, or manually reviewed behavioral oracle. Automated oracles are preferred.

## Baseline Features

The seed artifact includes a simple baseline feature extractor rather than a
full model claim. `scripts/baseline_features.py` computes patch/task overlap
features such as changed-file overlap, changed-line counts, changed-token
Jaccard similarity, and task-token Jaccard similarity. These features provide
transparent first baselines for same-file, patch-size, and task-similarity risk
heuristics.

## Quality Control

Before inclusion, verify:

1. The base commit is pinned.
2. Patch A and Patch B apply cleanly to the base.
3. Patch A and Patch B pass independently.
4. Patch A + Patch B merge without textual conflict.
5. The composed version fails a specific oracle.
6. The failure disappears when either patch is removed.
7. The failure is not caused by flaky tests or setup.
8. The conflict label is reviewed.
9. Reproduction commands are documented.
10. The instance runs in a fresh environment.
