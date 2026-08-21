# Task B: Reuse old-style escaping for simple format fields

## Problem

Markup has multiple formatting paths, and simple new-style format fields should
reuse the same escaping behavior as the older helper where practical.

## Desired behavior

Refactor simple `Markup.format` field handling to use the old-style escape
helper.

## Constraints

The public behavior of simple format fields should remain compatible with
existing `Markup.format` expectations.

## Success criteria

Simple fields such as `Markup("{}").format(value)` still escape unsafe input
and preserve normal Python stringification behavior.
