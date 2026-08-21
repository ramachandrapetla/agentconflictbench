# httpx__003: header key casing vs. update deduplication

This is the third HTTPX AgentConflictBench instance and the first
`state_invariant` seed.

## Repository

- Upstream: https://github.com/encode/httpx
- Base commit: `b5addb64f0161ff6bfe94c124ef76f6a1fba5254`
- Language: Python
- Conflict type: state_invariant
- Source: researcher_constructed

## Task A

Preserve original header casing when exposing `Headers.keys()`.

Example: `Headers([("X-Token", "one")]).keys()` returns `"X-Token"` rather
than the normalized lowercase lookup key.

Patch A passes its validation oracle.

## Task B

Optimize `Headers.update()` by removing existing entries through direct
normalized-key matching instead of calling `pop()` for each incoming header.

Example: updating `{"X-Token": "old"}` with `{"x-token": "new"}` still leaves
a single logical `x-token` value.

Patch B passes its validation oracle.

## Composition Failure

When Patch A and Patch B are composed, `Headers.update()` receives original-case
keys from the incoming headers but Patch B compares them directly against the
normalized lookup key stored in the existing header list.

As a result, updating `{"x-token": "old"}` with `{"X-Token": "new"}` leaves
both values in the internal list. The public `get_list("x-token")` API returns
`["old", "new"]` instead of `["new"]`.

The composition oracle captures the state invariant that update should replace
an existing logical header, not create a duplicate logical value because of key
casing.

## Why This Is An AgentConflictBench Instance

- Patch A is valid in isolation.
- Patch B is valid in isolation.
- Patch A and Patch B apply cleanly to the same base commit.
- The combined behavior fails a composition-level oracle.
- The failure comes from a broken internal invariant between header presentation
  casing and normalized lookup keys.

## Files

- `patch_a.patch`: preserve original header casing in `Headers.keys()`.
- `patch_b.patch`: optimize update deduplication through direct lookup-key matching.
- `oracle/test_patch_a.py`: Patch A validation oracle.
- `oracle/test_patch_b.py`: Patch B validation oracle.
- `oracle/test_composition.py`: composition failure oracle.
- `logs/`: validation outputs captured during seed creation.
