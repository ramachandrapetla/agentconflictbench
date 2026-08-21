# typer__001: TyperGroup command alias lookup vs. case-insensitive fallback

This is the first non-Click seeded AgentConflictBench instance.

## Repository

- Upstream: https://github.com/fastapi/typer
- Base commit: `9a7b2e83f6b62c750d6026b0de9ebf2026a8b8fa`
- Language: Python
- Conflict type: behavioral
- Source: researcher_constructed

## Task A

Allow `TyperGroup` command lookup to treat underscores in an invoked command name as aliases for dashes in registered command names.

Example: invoking `foo_bar` can resolve a registered command named `foo-bar`.

Patch A passes its validation oracle.

## Task B

Allow `TyperGroup` command lookup to fall back to lowercase command names when a mixed-case or uppercase command invocation is not found exactly.

Example: invoking `STATUS` can resolve a registered command named `status`.

Patch B passes its validation oracle.

## Composition Failure

When Patch A and Patch B are composed, their fallback mechanisms chain together. The invocation `FOO_BAR` is lowercased to `foo_bar`, then underscore-to-dash fallback resolves it to `foo-bar`.

The composition oracle expects `FOO_BAR` to remain unknown because neither patch independently admits the uppercase-underscore spelling for a dashed command.

Instead, the composed program succeeds and invokes `foo-bar`.

## Why This Is An AgentConflictBench Instance

- Patch A is valid in isolation.
- Patch B is valid in isolation.
- Patch A and Patch B apply cleanly to the same base commit.
- The combined behavior fails a composition-level oracle.
- The failure comes from transitive interaction between two independently plausible command-resolution fallbacks.

## Files

- `patch_a.diff`: underscore-to-dash command alias lookup in `TyperGroup`.
- `patch_b.diff`: lowercase command lookup fallback in `TyperGroup`.
- `oracle/test_patch_a.py`: Patch A validation oracle.
- `oracle/test_patch_b.py`: Patch B validation oracle.
- `oracle/test_composition.py`: composition failure oracle.
- `logs/`: validation outputs captured during seed creation.
