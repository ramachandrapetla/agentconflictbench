# click__003: Registered command name sync vs. duplicate command-name check

This is the third seeded AgentConflictBench instance.

## Repository

- Upstream: https://github.com/pallets/click
- Base commit: `2c8cd3ac958a7eb316d67f2d316c27086c4c0369`
- Language: Python
- Conflict type: API contract
- Source: researcher_constructed

## Task A

When a command is registered under an explicit name, update the command object's public `name` to match the registered API name.

Example: registering a command named `internal` as `public` changes `cmd.name` to `public`.

Patch A passes its validation oracle.

## Task B

Reject registering a distinct command object when its public command name is already registered on the same group.

Example: after registering a command named `sync`, registering another distinct command object also named `sync` should raise an error, even if it is registered under an alias such as `sync-alias`.

Patch B passes its validation oracle.

## Composition Failure

When Patch A and Patch B are composed, Patch A mutates the command object's `name` before Patch B performs the duplicate-name check. A second command originally named `sync` is registered as `sync-alias`; Patch A changes its public name to `sync-alias`, so Patch B no longer sees the duplicate original name `sync`.

The composition oracle expects the duplicate-name error to be raised. Instead, the composed program accepts the duplicate command.

## Why This Is An AgentConflictBench Instance

- Patch A is valid in isolation.
- Patch B is valid in isolation.
- Patch A and Patch B apply cleanly to the same base commit.
- The combined behavior fails a composition-level oracle.
- The failure comes from an API-contract interaction between command naming and duplicate-registration validation.

## Files

- `patch_a.patch`: synchronize command object name with explicit registered name.
- `patch_b.patch`: reject duplicate public command names after registration.
- `oracle/test_patch_a.py`: Patch A validation oracle.
- `oracle/test_patch_b.py`: Patch B validation oracle.
- `oracle/test_composition.py`: composition failure oracle.
- `logs/`: validation outputs captured during seed creation.
