# rich__003: blank_copy span preservation vs. copy helper refactor

This is the third Rich AgentConflictBench instance.

## Repository

- Upstream: https://github.com/Textualize/rich
- Base commit: `9d8f9a372cc5916fd4781fec207ced7ddac2f08f`
- Language: Python
- Conflict type: state_invariant
- Source: researcher_constructed

## Task A

Allow `blank_copy()` to preserve spans when replacement plain text is supplied.

Patch A passes its validation oracle.

## Task B

Refactor `Text.copy()` through `blank_copy()` and `copy_styles()`.

Patch B passes its validation oracle.

## Composition Failure

When Patch A and Patch B are composed, `blank_copy(self.plain)` already copies
spans and `copy_styles(self)` copies the same spans again.

The composition oracle expects `copy()` to preserve each span exactly once.

## Why This Is An AgentConflictBench Instance

- Patch A is valid in isolation.
- Patch B is valid in isolation.
- Patch A and Patch B apply cleanly to the same base commit.
- The combined behavior fails a composition-level oracle.
- The failure comes from a helper contract changed underneath a refactor.

## Files

- `task_a.md`: standalone intent for Patch A.
- `task_b.md`: standalone intent for Patch B.
- `patch_a.patch`: reference implementation for Patch A.
- `patch_b.patch`: reference implementation for Patch B.
- `combined.patch`: Patch A and Patch B applied together.
- `oracle/test_patch_a.py`: Patch A validation oracle.
- `oracle/test_patch_b.py`: Patch B validation oracle.
- `oracle/test_composition.py`: composition failure oracle.
- `logs/`: validation outputs captured during seed creation.
