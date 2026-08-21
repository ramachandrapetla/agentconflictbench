# rich__001: right-padding style extension vs. truncate padding delegation

This is the first Rich AgentConflictBench instance.

## Repository

- Upstream: https://github.com/Textualize/rich
- Base commit: `9d8f9a372cc5916fd4781fec207ced7ddac2f08f`
- Language: Python
- Conflict type: behavioral
- Source: researcher_constructed

## Task A

Improve `Text.pad_right()` so a trailing inline style span extends across
padding added to the right.

Example: padding `[red]x[/red]` by two cells produces plain text `x  ` with
the red span covering all three characters.

Patch A passes its validation oracle.

## Task B

Refactor `Text.truncate(..., pad=True)` to use `pad_right()` instead of
manually appending spaces.

This keeps padding length bookkeeping centralized while preserving the existing
contract that truncation padding itself remains unstyled.

Patch B passes its validation oracle.

## Composition Failure

When Patch A and Patch B are composed, `truncate(..., pad=True)` delegates to
`pad_right()`, and `pad_right()` now extends trailing style spans over padding.

As a result, truncating `[red]x[/red]` to width `3` with `pad=True` produces a
span covering `x  ` instead of only `x`.

The composition oracle expects truncation padding to remain unstyled.

## Why This Is An AgentConflictBench Instance

- Patch A is valid in isolation.
- Patch B is valid in isolation.
- Patch A and Patch B apply cleanly to the same base commit.
- The combined behavior fails a composition-level oracle.
- The failure comes from an implicit behavioral contract around padding style.

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
