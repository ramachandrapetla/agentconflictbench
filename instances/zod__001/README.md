# zod__001: metadata id inheritance vs. wrapper metadata inheritance

This is the first Zod AgentConflictBench instance.

## Repository

- Upstream: https://github.com/colinhacks/zod
- Base commit: `e516c3baf22615e20934116abebfed6c000222c2`
- Language: TypeScript
- Conflict type: api_contract
- Source: researcher_constructed

## Task A

Allow metadata IDs to be inherited across clone-derived schema variants.

Example: `z.string().meta({ id: "UserName" }).describe("User name")` keeps
the `id` metadata on the described clone.

Patch A passes its validation oracle.

## Task B

Make wrapper schemas inherit descriptive metadata from their inner schema.

Example: `z.string().meta({ description: "User name" }).optional()` exposes
the inherited description on the optional wrapper, while still suppressing
the inner schema's registration `id`.

Patch B passes its validation oracle.

## Composition Failure

When Patch A and Patch B are composed, optional wrappers inherit metadata from
their inner schemas and registry lookup no longer removes inherited `id`
fields.

As a result, `z.string().meta({ id: "UserName" }).optional().meta()?.id`
returns `"UserName"` instead of `undefined`.

The composition oracle expects wrapper schemas not to inherit registration IDs,
because IDs are used as schema identity/reference keys and should not silently
bubble into derived wrappers.

## Why This Is An AgentConflictBench Instance

- Patch A is valid in isolation.
- Patch B is valid in isolation.
- Patch A and Patch B apply cleanly to the same base commit.
- The combined behavior fails a composition-level oracle.
- The failure comes from an implicit metadata/registry contract.

## Files

- `patch_a.patch`: inherited metadata keeps `id` fields.
- `patch_b.patch`: optional wrappers inherit metadata from their inner schema.
- `oracle/test_patch_a.ts`: Patch A validation oracle.
- `oracle/test_patch_b.ts`: Patch B validation oracle.
- `oracle/test_composition.ts`: composition failure oracle.
- `logs/`: validation outputs captured during seed creation.
