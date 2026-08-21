# Task B: Lowercase fallback for Typer command lookup

## Problem

Users sometimes invoke Typer commands with uppercase or mixed-case spelling even
when the intended command is registered in lowercase.

## Desired behavior

Allow `TyperGroup` lookup to fall back to lowercase command names after exact
lookup fails.

## Constraints

Exact matches should still win. The fallback should not change registration
names or help text.

## Success criteria

A Typer app containing `status` can resolve an invocation of `STATUS` to the
registered `status` command.
