# Task B: Delegate array nonempty through min

## Problem

Array `.nonempty()` duplicates the minimum-length check created by `.min(1)`.

## Desired behavior

Refactor array `.nonempty()` to delegate to `.min(1)`.

## Constraints

The refactor should preserve other existing cardinality constraints on the
schema, including maximum length checks.

## Success criteria

`z.array(z.string()).max(1).nonempty()` rejects both empty arrays and arrays
with more than one element.
