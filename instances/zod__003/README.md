# zod__003: Array min replacement vs. nonempty delegation

## Repository

- Upstream: https://github.com/colinhacks/zod
- Base commit: `e516c3baf22615e20934116abebfed6c000222c2`
- Language: TypeScript
- Conflict type: state_invariant
- Source: researcher_constructed

## Task A

Change array `.min()` so a newly requested minimum-length policy replaces
existing array-length checks.

## Task B

Refactor array `.nonempty()` to delegate to `.min(1)` while preserving other
array cardinality constraints.

## Composition Failure

Patch B routes `.nonempty()` through `.min(1)`. Patch A changes `.min()` to
clear existing checks. Together, `.max(1).nonempty()` loses the max constraint
and accepts arrays with two elements.

## Files

- `task_a.md` and `task_b.md`: standalone task intents.
- `patch_a.patch` and `patch_b.patch`: reference implementations.
- `combined.patch`: clean textual composition.
- `oracle/`: Patch A, Patch B, and composition oracles.
- `scripts/`: reproduction helper scripts.
- `logs/`: captured validation outputs.
