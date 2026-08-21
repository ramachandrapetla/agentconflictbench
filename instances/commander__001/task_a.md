# Task A: Unique-prefix Commander subcommands

## Problem

Commander subcommands can have long names, and users may expect an
unambiguous abbreviation to resolve to the intended command.

## Desired behavior

Allow subcommand lookup to resolve a command-name prefix when exactly one
registered subcommand matches that prefix.

## Constraints

Ambiguous prefixes must not execute a command silently. Exact subcommand names
should keep their current behavior.

## Success criteria

If `status` is the only subcommand beginning with `sta`, invoking `sta` runs the
`status` subcommand.
