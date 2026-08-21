# <instance_id>: <short conflict title>

Briefly describe the instance in one sentence.

## Repository

- Upstream: <https://github.com/owner/repo>
- Base commit: `<40-character-sha>`
- Language: `<language>`
- Conflict type: `<conflict_type>`
- Source: `<source>`

## Task A

Describe the standalone intent for Patch A. This should match `task_a.md`.

Patch A passes its validation oracle.

## Task B

Describe the standalone intent for Patch B. This should match `task_b.md`.

Patch B passes its validation oracle.

## Composition Failure

Explain why Patch A and Patch B fail when composed. Name the hidden contract,
state invariant, precedence rule, API convention, or behavioral assumption that
both patches interact through.

## Why This Is An AgentConflictBench Instance

- Patch A is valid in isolation.
- Patch B is valid in isolation.
- Patch A and Patch B apply cleanly to the same base commit.
- The combined behavior fails a composition-level oracle.
- The failure is caused by patch interaction, not setup or flakiness.

## Files

- `task_a.md`: standalone intent for Patch A.
- `task_b.md`: standalone intent for Patch B.
- `patch_a.patch`: reference implementation for Task A.
- `patch_b.patch`: reference implementation for Task B.
- `combined.patch`: clean textual composition of Patch A and Patch B.
- `oracle/test_patch_a.*`: Patch A validation oracle.
- `oracle/test_patch_b.*`: Patch B validation oracle.
- `oracle/test_composition.*`: composition failure oracle.
- `logs/`: validation outputs captured during seed creation.
