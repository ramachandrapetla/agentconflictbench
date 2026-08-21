# Task B: Delegate loose object mode through catchall

## Problem

Object `.loose()` duplicates cloning logic that is also represented by setting a
catchall schema of `z.unknown()`.

## Desired behavior

Refactor object `.loose()` to delegate to `.catchall(z.unknown())`.

## Constraints

The refactor should preserve existing object-level refinements and public loose
mode behavior.

## Success criteria

`z.object(...).refine(...).loose()` still runs the refinement while allowing
unknown keys.
