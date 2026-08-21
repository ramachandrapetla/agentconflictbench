# markupsafe__001: silent old-style None formatting vs. new-style helper reuse

This is the first MarkupSafe AgentConflictBench instance.

## Repository

- Upstream: https://github.com/pallets/markupsafe
- Base commit: `b2e4d9c7687be25695fffbe93a37622302b24fb1`
- Language: Python
- Conflict type: test_assumption
- Source: researcher_constructed

## Task A

Make old-style `Markup` formatting treat `None` as an empty optional value.

Example: `Markup("%s") % None` returns `Markup("")`.

Patch A passes its validation oracle.

## Task B

Refactor simple `Markup.format()` fields so they reuse the same escape helper
used by old-style `%` formatting.

Example: `Markup("<{}>").format("<x>")` still escapes the inserted value, and
`Markup("{}").format(None)` still renders `Markup("None")`.

Patch B passes its validation oracle.

## Composition Failure

When Patch A and Patch B are composed, new-style formatting starts using the
old-style helper whose `None` behavior changed.

As a result, `Markup("{}").format(None)` returns an empty string instead of
`Markup("None")`.

The composition oracle preserves the existing new-style formatting assumption
that `None` stringifies as the literal text `None`.

## Why This Is An AgentConflictBench Instance

- Patch A is valid in isolation.
- Patch B is valid in isolation.
- Patch A and Patch B apply cleanly to the same base commit.
- The combined behavior fails a composition-level oracle.
- The failure comes from a formatting-helper reuse assumption.

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
