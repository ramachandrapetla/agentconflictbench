# rich__004: divide metadata-only segmentation vs. split delegation

This is the fourth Rich AgentConflictBench instance.

## Repository

- Upstream: https://github.com/Textualize/rich
- Base commit: `9d8f9a372cc5916fd4781fec207ced7ddac2f08f`
- Language: Python
- Conflict type: behavioral
- Source: researcher_constructed

## Task A

Make `divide([])` return a metadata-only segment without inline spans.

Patch A passes its validation oracle.

## Task B

Refactor `split()` so the no-separator branch delegates to `divide([])`.

Patch B passes its validation oracle because base `divide([])` returns a normal
copy that preserves spans.

## Composition Failure

When Patch A and Patch B are composed, splitting text on a separator that is not
present now returns the new metadata-only `divide([])` segment.

The composition oracle expects `split()` to preserve spans when no split occurs.

## Why This Is An AgentConflictBench Instance

- Patch A is valid in isolation.
- Patch B is valid in isolation.
- Patch A and Patch B apply cleanly to the same base commit.
- The combined behavior fails a composition-level oracle.
- The failure comes from changed helper semantics beneath a public API refactor.

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
