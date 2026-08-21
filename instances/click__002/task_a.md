# Task A: Underscore aliases for dashed command names

## Problem

Click commands are commonly registered with dashed names, but users sometimes
type underscores when invoking command names from scripts or generated tools.

## Desired behavior

Allow command lookup to treat underscores in an invoked command name as aliases
for dashes in registered command names.

## Constraints

Exact command-name matches should keep their current behavior. The alias should
only be used as a fallback when the invoked name is not found directly.

## Success criteria

A group containing `foo-bar` can resolve an invocation of `foo_bar` to the same
command.
