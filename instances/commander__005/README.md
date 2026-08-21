# commander__005: Negated option classification vs. value branch ordering

## Repository

- Upstream: https://github.com/tj/commander.js
- Base commit: `ba6d13ddb4243e5913367734f8c159089ffe7834`
- Language: JavaScript
- Conflict type: behavioral
- Source: researcher_constructed

## Task A

Classify negated options such as `--no-cache` as boolean options so option
inspection treats regular boolean flags and negated boolean flags uniformly.

## Task B

Simplify option value handling by resolving boolean and optional options before
the dedicated negated-option branch, while preserving `--no-*` behavior.

## Composition Failure

Patch A makes `--no-cache` satisfy `isBoolean()`. Patch B checks `isBoolean()`
before checking `option.negate`. Together, `--no-cache` is resolved as `true`
instead of the expected `false`.

## Files

- `task_a.md` and `task_b.md`: standalone task intents.
- `patch_a.patch` and `patch_b.patch`: reference implementations.
- `combined.patch`: clean textual composition.
- `oracle/`: Patch A, Patch B, and composition oracles.
- `scripts/`: reproduction helper scripts.
- `logs/`: captured validation outputs.
