# Task B: Delegate Markup construction through escape

## Problem

Constructing `Markup` from HTML-aware objects duplicates conversion behavior
that already exists in `escape`.

## Desired behavior

Delegate `Markup` construction for HTML-aware objects through `escape`.

## Constraints

The constructor should preserve the established `Markup(obj)` protocol for
HTML-aware objects and should not double-escape safe HTML.

## Success criteria

Constructing `Markup` from an object with `__html__` still produces the object's
safe HTML representation.
