# Task B: Reuse right-padding helper in truncate padding

## Problem

`Text.truncate(..., pad=True)` has padding logic that overlaps with the
existing right-padding helper.

## Desired behavior

Refactor truncate padding to delegate to the existing right-padding helper.

## Constraints

The visible output of truncation with padding should remain unchanged,
including the style behavior of padding spaces.

## Success criteria

Truncating text with `pad=True` returns the requested width and keeps padding
spaces unstyled unless existing truncate behavior says otherwise.
