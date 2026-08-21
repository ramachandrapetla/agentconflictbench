# Task A: Treat None as empty in old-style Markup formatting

## Problem

Old-style Markup formatting may receive optional values that are represented as
`None`, and rendering the literal string `"None"` can be undesirable in HTML
templates.

## Desired behavior

Make old-style Markup formatting treat `None` as an empty optional value.

## Constraints

Other values should continue to be escaped normally. This change should be
limited to the old-style formatting helper path.

## Success criteria

Formatting a Markup template with `% None` produces an empty escaped value
rather than the text `None`.
