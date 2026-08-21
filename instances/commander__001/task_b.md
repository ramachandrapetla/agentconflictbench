# Task B: Lowercase fallback for Commander subcommands

## Problem

Users may type Commander subcommands with uppercase or mixed-case spelling even
when the registered subcommand is lowercase.

## Desired behavior

When exact subcommand dispatch fails, retry lookup with the lowercase invoked
subcommand name.

## Constraints

Exact matches should still take priority. The fallback should not change
registered command names or help output.

## Success criteria

A program containing a `status` subcommand can dispatch an invocation of
`STATUS` to `status`.
