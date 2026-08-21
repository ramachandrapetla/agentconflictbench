# Task A: Preserve appended Text end metadata in append_text

## Problem

Internal text appends may drop the appended `Text` object's end metadata, which
can matter for downstream rendering or line-ending behavior.

## Desired behavior

Make `append_text` preserve the appended `Text` object's end metadata.

## Constraints

The appended plain text and spans should continue to be copied as before.
Metadata preservation should be limited to the internal append helper.

## Success criteria

Appending a `Text` object through `append_text` carries over that object's end
metadata.
