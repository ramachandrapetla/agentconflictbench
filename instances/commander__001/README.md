# commander__001: Prefix subcommand lookup vs. lowercase fallback

This is the first JavaScript AgentConflictBench instance.

## Repository

- Upstream: https://github.com/tj/commander.js
- Base commit: `ba6d13ddb4243e5913367734f8c159089ffe7834`
- Language: JavaScript
- Conflict type: behavioral
- Source: researcher_constructed

## Task A

Allow Commander subcommand lookup to resolve a command-name prefix when the
prefix uniquely matches one registered subcommand.

Example: invoking `sta` can resolve a registered command named `status`.

Patch A passes its validation oracle.

## Task B

Allow Commander subcommand dispatch to fall back to lowercase command names
when an uppercase or mixed-case invocation is not found exactly.

Example: invoking `STATUS` can resolve a registered command named `status`.

Patch B passes its validation oracle.

## Composition Failure

When Patch A and Patch B are composed, the invocation `STA` is lowercased to
`sta`, then unique-prefix lookup resolves it to `status`.

The composition oracle expects uppercase abbreviations to remain invalid,
because neither patch independently admits that combined invocation form.
Instead, the composed Commander program succeeds and invokes `status`.

## Why This Is An AgentConflictBench Instance

- Patch A is valid in isolation.
- Patch B is valid in isolation.
- Patch A and Patch B apply cleanly to the same base commit.
- The combined behavior fails a composition-level oracle.
- The failure comes from transitive interaction between two independently
  plausible subcommand-resolution fallbacks.

## Files

- `patch_a.diff`: unique-prefix subcommand lookup.
- `patch_b.diff`: lowercase subcommand dispatch fallback.
- `oracle/test_patch_a.mjs`: Patch A validation oracle.
- `oracle/test_patch_b.mjs`: Patch B validation oracle.
- `oracle/test_composition.mjs`: composition failure oracle.
- `logs/`: validation outputs captured during seed creation.
