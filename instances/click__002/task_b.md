# Task B: Lowercase fallback for command lookup

## Problem

Users may invoke commands with accidental uppercase or mixed-case spelling even
when the registered command name is lowercase.

## Desired behavior

Allow command lookup to fall back to a lowercase command name when the original
invocation is not found exactly.

## Constraints

Exact case-sensitive matches must continue to win. The fallback should not
change command registration or display names.

## Success criteria

A group containing `status` can resolve an invocation of `STATUS` to the
registered command.
