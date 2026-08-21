# Task A: Preserve spans in blank_copy with replacement text

## Problem

`blank_copy` can be useful for creating a new `Text` object with replacement
plain text, but dropping spans loses style structure callers may want to keep.

## Desired behavior

Allow `blank_copy` to preserve spans when replacement plain text is provided.

## Constraints

Span preservation should not duplicate spans. Existing blank-copy behavior
without replacement text should remain compatible.

## Success criteria

Calling `blank_copy` with replacement plain text can produce a copy that keeps
the original spans.
