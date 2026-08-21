# Task B: Route split without separators through divide

## Problem

`Text.split` has a no-separator branch that overlaps with `divide` behavior for
producing text segments.

## Desired behavior

Refactor the no-separator branch of `split` to use `divide([])`.

## Constraints

Splitting on a separator that is not present should preserve the original text
and spans exactly as before.

## Success criteria

Splitting styled text on a missing separator returns one segment with the same
plain text and inline spans as the original.
