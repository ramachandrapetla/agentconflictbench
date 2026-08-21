# Task B: Delegate QueryParams.get through mapping access

## Problem

`QueryParams.get`, membership checks, and item access can drift if each path
implements lookup logic separately.

## Desired behavior

Refactor `QueryParams.get` to delegate through the mapping protocol so `get`,
`in`, and item access share behavior.

## Constraints

`get` should still return the provided default when the key is absent. Existing
exact-key lookups should remain compatible.

## Success criteria

`params.get("name", default)` returns the same value as item access for present
keys and returns `default` for missing keys.
