# Task A: Underscore aliases for dashed Typer commands

## Problem

Typer command names often use dashes, while programmatic callers and scripts may
produce underscores.

## Desired behavior

Allow `TyperGroup` command lookup to treat underscores in the invoked command
name as aliases for dashes in registered command names.

## Constraints

Exact command lookup must remain unchanged. The alias should be a fallback and
should not alter help output or registered command names.

## Success criteria

A Typer command registered as `foo-bar` can be invoked as `foo_bar` when no
exact `foo_bar` command exists.
