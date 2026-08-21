# Task A: False-like environment values for booleans

## Problem

Boolean options sourced from environment variables often receive string values
such as `false`, `0`, or `no`, which should be interpreted as false rather than
truthy strings.

## Desired behavior

Treat common false-like environment values for boolean options as boolean
`false`.

## Constraints

The change should apply to boolean options loaded from environment values and
should not alter parsing of non-boolean option values.

## Success criteria

An environment variable such as `DEBUG=false` produces `debug: false` for a
boolean option.
