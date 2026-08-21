# Task A: Unique command-prefix lookup

## Problem

Long command names are inconvenient to type, and some CLIs allow users to invoke
a command by an unambiguous prefix.

## Desired behavior

Allow command lookup to resolve a command-name prefix when it uniquely matches a
registered command.

## Constraints

Ambiguous prefixes must not resolve silently. Exact command names should keep
their current behavior.

## Success criteria

If only `status` matches the prefix `sta`, invoking `sta` runs `status`; if more
than one command matches, lookup remains unresolved or reports ambiguity.
