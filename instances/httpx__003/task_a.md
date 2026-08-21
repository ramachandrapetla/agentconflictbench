# Task A: Preserve original header casing in keys

## Problem

HTTP header lookup is case-insensitive, but callers sometimes need to inspect
the original casing used when headers were provided.

## Desired behavior

Expose original header casing from `Headers.keys()`.

## Constraints

Case-insensitive lookup behavior should remain unchanged. The change should
affect the public key view, not header normalization for lookup.

## Success criteria

If headers are created with `X-Trace`, iterating `headers.keys()` includes
`X-Trace`.
