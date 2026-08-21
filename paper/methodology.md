# Benchmark Methodology

AgentConflictBench uses a hybrid construction strategy. Pure mining may miss silent semantic failures because they do not appear as Git conflicts. Pure manual construction risks looking artificial. The benchmark therefore combines mined, agent-generated, and researcher-constructed task pairs.

## Construction Pipeline

1. Select repositories.
2. Generate or identify independent task pairs.
3. Produce candidate patches from the same base commit.
4. Validate each patch independently.
5. Compose patch pairs and detect clean-merge failures.
6. Label, audit, and package accepted instances.

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

## Composition Oracle

A composition-level oracle may be a unit test, integration test, property-based test, regression test, static policy check, controlled performance threshold, or manually reviewed behavioral oracle. Automated oracles are preferred.

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
