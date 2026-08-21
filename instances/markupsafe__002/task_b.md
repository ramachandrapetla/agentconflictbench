# Task B: Use soft_str for escape fallback conversion

## Problem

`escape` and `soft_str` can diverge when converting non-string values before
HTML escaping.

## Desired behavior

Refactor `escape` so its non-string fallback conversion goes through
`soft_str`.

## Constraints

HTML-aware objects and existing Markup values should keep their specialized
handling. The refactor should preserve escaping of unsafe characters.

## Success criteria

Escaping an ordinary non-string value converts it through the shared soft string
path and still escapes HTML-sensitive characters.
