# rich__002: append_text end inheritance vs. public append delegation

This is the second Rich AgentConflictBench instance.

## Repository

- Upstream: https://github.com/Textualize/rich
- Base commit: `9d8f9a372cc5916fd4781fec207ced7ddac2f08f`
- Language: Python
- Conflict type: api_contract
- Source: researcher_constructed

## Task A

Make the low-level `Text.append_text()` helper preserve the appended `Text`
object's `end` metadata.

Example: `Text("left", end="\n").append_text(Text("right", end=""))` leaves the
combined object with `end == ""`.

Patch A passes its validation oracle.

## Task B

Refactor public `Text.append(Text)` so it reuses `append_text()` instead of
duplicating the span-copying implementation.

Public `append(Text)` should still preserve the receiver's own `end` value.

Patch B passes its validation oracle.

## Composition Failure

When Patch A and Patch B are composed, public `append(Text)` delegates to
`append_text()`, and `append_text()` now copies the appended object's `end`.

As a result, `Text("left", end="!").append(Text("right", end="?"))` changes the
receiver's `end` from `!` to `?`.

The composition oracle expects public `append(Text)` not to inherit appended
line-ending metadata.

## Why This Is An AgentConflictBench Instance

- Patch A is valid in isolation.
- Patch B is valid in isolation.
- Patch A and Patch B apply cleanly to the same base commit.
- The combined behavior fails a composition-level oracle.
- The failure comes from an implicit public API contract around mutable metadata.

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
