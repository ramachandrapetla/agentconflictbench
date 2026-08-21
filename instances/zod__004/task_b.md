# Task B: Delegate set nonempty through min

## Problem

Set `.nonempty()` duplicates the minimum-size check created by `.min(1)`.

## Desired behavior

Refactor set `.nonempty()` to delegate to `.min(1)`.

## Constraints

The refactor should preserve other existing cardinality constraints on the
schema, including maximum size checks.

## Success criteria

`z.set(z.string()).max(1).nonempty()` rejects both empty sets and sets with more
than one value.
