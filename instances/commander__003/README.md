# commander__003: conflicts flag aliases vs. implies flag aliases

This is the third Commander.js AgentConflictBench instance.

## Repository

- Upstream: https://github.com/tj/commander.js
- Base commit: `ba6d13ddb4243e5913367734f8c159089ffe7834`
- Language: JavaScript
- Conflict type: API contract
- Source: researcher_constructed

## Task A

Allow `Option.conflicts()` to accept long option flag spellings, such as
`--cache-dir`, as aliases for Commander option attribute names, such as
`cacheDir`.

Patch A passes its validation oracle.

## Task B

Allow `Option.implies()` to accept long option flag spellings, such as
`--cache-dir`, and normalize them to Commander option attribute names when
setting implied option values.

Patch B passes its validation oracle.

## Composition Failure

When Patch A and Patch B are composed, an option can both conflict with and
imply the same long flag spelling:

```js
new Option('--offline')
  .conflicts('--cache-dir')
  .implies({ '--cache-dir': './cache' });
```

Patch A makes the conflict reference resolve to `cacheDir`. Patch B makes the
implied value resolve to `cacheDir`. Together, Commander reports a conflict
when the user only supplies `--offline`, even though `--cache-dir` was not
provided by the user.

## Why This Is An AgentConflictBench Instance

- Patch A is valid in isolation.
- Patch B is valid in isolation.
- Patch A and Patch B apply cleanly to the same base commit.
- The combined behavior fails a composition-level oracle.
- The failure comes from two independently reasonable API-normalization changes
  sharing a hidden attribute-name convention.

## Files

- `task_a.md`: standalone intent for Patch A.
- `task_b.md`: standalone intent for Patch B.
- `patch_a.patch`: normalize long flag spellings in `conflicts()`.
- `patch_b.patch`: normalize long flag spellings in `implies()`.
- `combined.patch`: clean textual composition of Patch A and Patch B.
- `oracle/test_patch_a.mjs`: Patch A validation oracle.
- `oracle/test_patch_b.mjs`: Patch B validation oracle.
- `oracle/test_composition.mjs`: composition failure oracle.
- `logs/`: validation outputs captured during seed creation.
