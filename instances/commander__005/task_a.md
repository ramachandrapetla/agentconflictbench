# Task A: Classify negated options as boolean options

## Problem

Negated options such as `--no-cache` behave like boolean flags but may not be
reported as boolean options by generic option-inspection code.

## Desired behavior

Update boolean option classification so negated options are treated as boolean
options.

## Constraints

Required and optional value-taking options should not be classified as plain
boolean options. Runtime behavior of `--no-*` flags should remain unchanged.

## Success criteria

`new Option("--no-cache").isBoolean()` returns true, and parsing `--no-cache`
still sets `cache` to false.
