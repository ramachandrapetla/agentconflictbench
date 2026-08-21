# Task A: Dashed default-map option aliases

## Problem

Click stores option parameter names internally with underscores, but users often
write configuration files with CLI-style dashed keys such as `api-key`.

## Desired behavior

Allow `Context.default_map` to resolve dashed option names as aliases for their
underscored parameter names.

## Constraints

Existing underscored keys must continue to work. The change should only affect
default-map lookup and should not alter command-line parsing or environment
variable naming.

## Success criteria

A command option declared as `--api-key` can receive its default from either
`{"api_key": "..."}` or `{"api-key": "..."}` in `default_map`.
