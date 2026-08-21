# Task A: Replace set-size checks in min

## Problem

Applying a new set `.min()` constraint may be intended to replace prior set-size
policy rather than accumulate with older size checks.

## Desired behavior

When applying a new set `.min()` constraint, replace existing set-size checks
before adding the new minimum.

## Constraints

The resulting schema must still enforce the requested minimum size. Other set
behavior should remain unchanged.

## Success criteria

`z.set(z.string()).max(1).min(1)` accepts a two-value set but still rejects an
empty set.
