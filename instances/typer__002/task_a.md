# Task A: Unique-prefix Typer command lookup

## Problem

Typer command names may be long, and users sometimes expect unambiguous
abbreviations to work.

## Desired behavior

Allow a Typer command invocation to resolve a uniquely matching command-name
prefix.

## Constraints

Ambiguous prefixes must not execute a command silently. Exact command names
should preserve their current behavior.

## Success criteria

If `status` is the only registered command beginning with `sta`, invoking `sta`
resolves to `status`.
