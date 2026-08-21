# Task B: Optimize Headers.update normalized-key removal

## Problem

Updating headers should remove any existing logical header before inserting the
new value, and this path can be optimized by comparing normalized keys directly.

## Desired behavior

Refactor `Headers.update` to remove existing entries through direct
normalized-key matching.

## Constraints

Updating with different casing should still replace the old logical header
rather than creating duplicates.

## Success criteria

Updating `{"X-Trace": "one"}` with `{"x-trace": "two"}` leaves one logical
header value, `two`.
