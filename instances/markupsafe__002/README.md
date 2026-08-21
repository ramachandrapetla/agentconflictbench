# markupsafe__002: bytes-aware soft_str vs. escape fallback delegation

This is the second MarkupSafe AgentConflictBench instance.

## Repository

- Upstream: https://github.com/pallets/markupsafe
- Base commit: `b2e4d9c7687be25695fffbe93a37622302b24fb1`
- Language: Python
- Conflict type: api_contract
- Source: researcher_constructed

## Task A

Teach `soft_str()` to decode byte strings as UTF-8 text.

Example: `soft_str(b"<x>")` returns `"<x>"`.

Patch A passes its validation oracle and leaves `escape(bytes)` unchanged.

## Task B

Refactor `escape()` to use `soft_str()` for non-string fallback conversion.

Patch B passes its validation oracle because the existing `soft_str(bytes)`
behavior still delegates to Python's `str(bytes)` representation.

## Composition Failure

When Patch A and Patch B are composed, `escape(bytes)` starts using the new
bytes-decoding behavior from `soft_str()`.

As a result, `escape(b"<x>")` returns `Markup("&lt;x&gt;")` instead of
`Markup("b&#39;&lt;x&gt;&#39;")`.

The composition oracle expects `escape(bytes)` to preserve the existing public
conversion contract based on Python's bytes representation.

## Why This Is An AgentConflictBench Instance

- Patch A is valid in isolation.
- Patch B is valid in isolation.
- Patch A and Patch B apply cleanly to the same base commit.
- The combined behavior fails a composition-level oracle.
- The failure comes from a helper-delegation interaction in conversion logic.

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
