# Task A: Metadata-only divide result with no offsets

## Problem

Dividing text with no offsets can still require a segment that preserves text
metadata even when no inline span slicing is needed.

## Desired behavior

Make `divide([])` return a metadata-only segment when no offsets are provided.

## Constraints

The no-offset behavior should not introduce inline spans into the returned
segment. Existing divide behavior with offsets should remain unchanged.

## Success criteria

Calling `divide([])` returns a single segment that preserves relevant metadata
without inline spans.
