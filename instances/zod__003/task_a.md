# Task A: Replace array-length checks in min

## Problem

Applying a new array `.min()` constraint may be intended to replace prior
array-length policy rather than accumulate with older length checks.

## Desired behavior

When applying a new array `.min()` constraint, replace existing array-length
checks before adding the new minimum.

## Constraints

The resulting schema must still enforce the requested minimum length. Other
array behavior should remain unchanged.

## Success criteria

`z.array(z.string()).max(1).min(1)` accepts a two-element array but still rejects
an empty array.
