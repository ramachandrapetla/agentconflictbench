# commander__004: Required argument defaults vs. optionalization helper cleanup

## Repository

- Upstream: https://github.com/tj/commander.js
- Base commit: `ba6d13ddb4243e5913367734f8c159089ffe7834`
- Language: JavaScript
- Conflict type: api_contract
- Source: researcher_constructed

## Task A

Allow `Argument.argOptional()` to clear any stale default value when converting
a required positional argument into an optional argument.

## Task B

Allow `Command.addArgument()` to accept a prepared required `Argument` with a
default value by treating that argument as optional, while preserving the
default as the fallback when the argument is omitted.

## Composition Failure

Patch B reuses `argOptional()`. Patch A changes `argOptional()` to clear
defaults. When composed, the registration no longer throws, but the fallback
value is silently discarded and the action receives `undefined`.

## Files

- `task_a.md` and `task_b.md`: standalone task intents.
- `patch_a.patch` and `patch_b.patch`: reference implementations.
- `combined.patch`: clean textual composition.
- `oracle/`: Patch A, Patch B, and composition oracles.
- `scripts/`: reproduction helper scripts.
- `logs/`: captured validation outputs.
