# Task B: Simplify missing option value resolution

## Problem

Commander has multiple branches for filling in missing option values, including
boolean, optional, and negated options.

## Desired behavior

Resolve boolean and optional options before falling through to the dedicated
negated-option value branch.

## Constraints

The public behavior of negated options must remain unchanged. Passing `--no-*`
without an explicit value should still produce false.

## Success criteria

A program with `--no-cache` still reports `cache: false` after parsing
`--no-cache`.
