# httpx__001: QueryParams membership vs. get delegation

This is the first HTTPX AgentConflictBench instance.

## Repository

- Upstream: https://github.com/encode/httpx
- Base commit: `b5addb64f0161ff6bfe94c124ef76f6a1fba5254`
- Language: Python
- Conflict type: api_contract
- Source: researcher_constructed

## Task A

Allow `QueryParams` membership checks to treat query parameter names
case-insensitively.

Example: `"token" in QueryParams({"Token": "abc"})` returns `True`.

Patch A passes its validation oracle.

## Task B

Refactor `QueryParams.get` to delegate through the mapping protocol, so
`get`, `in`, and `[]` access share behavior rather than duplicating dictionary
lookup logic.

Example: `QueryParams({"token": "abc"}).get("token")` still returns `"abc"`.

Patch B passes its validation oracle.

## Composition Failure

When Patch A and Patch B are composed, `QueryParams.__contains__` becomes
case-insensitive but `QueryParams.__getitem__` remains exact-key lookup.

As a result, `params.get("token", "missing")` first sees that `"token" in
params` is true, then calls `params["token"]`, which raises `KeyError` because
the stored key is `"Token"`.

The composition oracle expects the API to keep returning the caller-provided
default for a non-exact `get` lookup. Instead, the composed implementation
raises.

## Why This Is An AgentConflictBench Instance

- Patch A is valid in isolation.
- Patch B is valid in isolation.
- Patch A and Patch B apply cleanly to the same base commit.
- The combined behavior fails a composition-level oracle.
- The failure comes from an implicit API contract between mapping methods.

## Files

- `patch_a.diff`: case-insensitive `QueryParams.__contains__`.
- `patch_b.diff`: `QueryParams.get` delegates via mapping protocol.
- `oracle/test_patch_a.py`: Patch A validation oracle.
- `oracle/test_patch_b.py`: Patch B validation oracle.
- `oracle/test_composition.py`: composition failure oracle.
- `logs/`: validation outputs captured during seed creation.
