# Task B: Refactor Text.copy through copy helpers

## Problem

`Text.copy` duplicates behavior that overlaps with `blank_copy` and style-copy
helpers.

## Desired behavior

Refactor `Text.copy` to use `blank_copy` and `copy_styles` helper paths.

## Constraints

The public copy result should remain semantically identical: same plain text,
same spans, and no duplicate style ranges.

## Success criteria

Copying a `Text` object produces exactly one copy of each original span.
