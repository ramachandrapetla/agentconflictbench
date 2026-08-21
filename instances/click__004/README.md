# click__004: Prefix command lookup vs. lowercase fallback

This is an expansion AgentConflictBench instance for Click.

## Repository

- Upstream: https://github.com/pallets/click
- Base commit: `2c8cd3ac958a7eb316d67f2d316c27086c4c0369`
- Language: Python
- Conflict type: behavioral
- Source: researcher_constructed

## Task A

Allow command lookup to resolve a command-name prefix when the prefix uniquely
matches one registered command.

Example: invoking `sta` can resolve a registered command named `status`.

Patch A passes its validation oracle.

## Task B

Allow command lookup to fall back to lowercase command names when an uppercase
or mixed-case invocation is not found exactly.

Example: invoking `STATUS` can resolve a registered command named `status`.

Patch B passes its validation oracle.

## Composition Failure

When Patch A and Patch B are composed, the invocation `STA` is lowercased to
`sta`, then unique-prefix lookup resolves it to `status`.

The composition oracle expects uppercase abbreviations to remain invalid,
because neither patch independently admits that combined invocation form.
Instead, the composed program succeeds and invokes `status`.

## Why This Is An AgentConflictBench Instance

- Patch A is valid in isolation.
- Patch B is valid in isolation.
- Patch A and Patch B apply cleanly to the same base commit.
- The combined behavior fails a composition-level oracle.
- The failure comes from transitive interaction between two independently
  plausible command-resolution fallbacks.

## Files

- `patch_a.diff`: unique-prefix command lookup.
- `patch_b.diff`: lowercase command lookup fallback.
- `oracle/test_patch_a.py`: Patch A validation oracle.
- `oracle/test_patch_b.py`: Patch B validation oracle.
- `oracle/test_composition.py`: composition failure oracle.
- `logs/`: validation outputs captured during seed creation.
