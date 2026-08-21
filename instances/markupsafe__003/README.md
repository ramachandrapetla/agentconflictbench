# markupsafe__003: html-format escape preference vs. constructor escape delegation

This is the third MarkupSafe AgentConflictBench instance.

## Repository

- Upstream: https://github.com/pallets/markupsafe
- Base commit: `b2e4d9c7687be25695fffbe93a37622302b24fb1`
- Language: Python
- Conflict type: api_contract
- Source: researcher_constructed

## Task A

Prefer `__html_format__("")` when direct escaping sees an object that supports
both `__html__` and `__html_format__`.

Patch A passes its validation oracle and leaves `Markup(obj)` construction on
the direct `__html__` path.

## Task B

Delegate `Markup` construction for HTML-aware objects through the central
`escape()` helper.

Patch B passes its validation oracle because the original `escape()` helper
still calls `__html__()`.

## Composition Failure

When Patch A and Patch B are composed, `Markup(obj)` starts using the new
`escape()` precedence and therefore calls `__html_format__("")` instead of
`__html__()`.

The composition oracle expects the constructor to preserve the established
`__html__` protocol contract.

## Why This Is An AgentConflictBench Instance

- Patch A is valid in isolation.
- Patch B is valid in isolation.
- Patch A and Patch B apply cleanly to the same base commit.
- The combined behavior fails a composition-level oracle.
- The failure comes from protocol-precedence interaction across helpers.

## Files

- `task_a.md`: standalone intent for Patch A.
- `task_b.md`: standalone intent for Patch B.
- `patch_a.patch`: reference implementation for Patch A.
- `patch_b.patch`: reference implementation for Patch B.
- `combined.patch`: Patch A and Patch B applied together.
- `oracle/test_patch_a.py`: Patch A validation oracle.
- `oracle/test_patch_b.py`: Patch B validation oracle.
- `oracle/test_composition.py`: composition failure oracle.
- `logs/`: validation outputs captured during seed creation.
