# commander__002: boolean env parsing vs. implied-option precedence

This is the second Commander.js AgentConflictBench instance.

## Repository

- Upstream: https://github.com/tj/commander.js
- Base commit: `ba6d13ddb4243e5913367734f8c159089ffe7834`
- Language: JavaScript
- Conflict type: configuration
- Source: researcher_constructed

## Task A

Treat common false-like environment values for boolean options as `false`.

Example: with `new Option("--debug").env("DEBUG")`, `DEBUG=false` sets
`debug` to `false` instead of treating the variable's mere presence as `true`.

Patch A passes its validation oracle.

## Task B

Allow implied option values to override environment/config-derived values.

Example: `--trace` can imply `{ log: "trace.log" }` even when `LOG=env.log`
is present, so a CLI mode flag can force a coherent configuration profile.

Patch B passes its validation oracle.

## Composition Failure

When Patch A and Patch B are composed, an explicit boolean environment setting
such as `DEBUG=false` becomes vulnerable to being overwritten by an implied
value such as `--trace.implies({ debug: true })`.

The composition oracle expects the explicit environment setting to remain
authoritative for the boolean option. Instead, the composed implementation
changes `debug` to `true`.

## Why This Is An AgentConflictBench Instance

- Patch A is valid in isolation.
- Patch B is valid in isolation.
- Patch A and Patch B apply cleanly to the same base commit.
- The combined behavior fails a composition-level oracle.
- The failure comes from an implicit precedence contract between environment
  configuration and implied options.

## Files

- `patch_a.diff`: parse false-like boolean env values as `false`.
- `patch_b.diff`: allow implied values to override env/config values.
- `oracle/test_patch_a.mjs`: Patch A validation oracle.
- `oracle/test_patch_b.mjs`: Patch B validation oracle.
- `oracle/test_composition.mjs`: composition failure oracle.
- `logs/`: validation outputs captured during seed creation.
