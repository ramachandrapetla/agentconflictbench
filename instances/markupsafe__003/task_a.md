# Task A: Prefer __html_format__ during escaping

## Problem

HTML-aware objects may define both `__html__` and `__html_format__`, and
format-aware escaping should prefer the richer formatting protocol when
available.

## Desired behavior

When escaping an HTML-aware object, prefer `__html_format__("")` over
`__html__`.

## Constraints

Objects that only define `__html__` should continue to work. The format string
passed for the default escape path should be empty.

## Success criteria

For an object implementing both methods, `escape(obj)` uses the result of
`obj.__html_format__("")`.
