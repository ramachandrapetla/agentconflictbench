# zod__002: Object catchall cleanup vs. loose-mode delegation

## Repository

- Upstream: https://github.com/colinhacks/zod
- Base commit: `e516c3baf22615e20934116abebfed6c000222c2`
- Language: TypeScript
- Conflict type: state_invariant
- Source: researcher_constructed

## Task A

When changing an object schema's catchall policy, clear existing object-level
refinements so the catchall variant validates independently.

## Task B

Refactor `.loose()` to delegate to `.catchall(z.unknown())` while preserving
object-level refinements.

## Composition Failure

Patch B routes `.loose()` through `.catchall()`. Patch A changes `.catchall()`
to clear checks. Together, `.loose()` silently drops object-level refinements
and accepts input the original loose schema would reject.

## Files

- `task_a.md` and `task_b.md`: standalone task intents.
- `patch_a.patch` and `patch_b.patch`: reference implementations.
- `combined.patch`: clean textual composition.
- `oracle/`: Patch A, Patch B, and composition oracles.
- `scripts/`: reproduction helper scripts.
- `logs/`: captured validation outputs.
