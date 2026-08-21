# Task B: Implied option values override configuration sources

## Problem

An option may imply another option value, and users expect that implication to
take effect even when the implied option has a value from environment or config.

## Desired behavior

Allow implied option values to override values derived from environment or
configuration sources.

## Constraints

Explicit user-supplied CLI values should still have the highest precedence. The
change should only affect implied values competing with lower-priority sources.

## Success criteria

When `--trace` implies `debug: true`, invoking `--trace` sets `debug` to true
even if `debug` already has an environment-derived value.
