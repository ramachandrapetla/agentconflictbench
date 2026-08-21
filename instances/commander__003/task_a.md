# Task A: Flag spelling aliases for option conflicts

## Problem

Commander option conflict declarations are easier to write with CLI flag
spellings such as `--cache-dir`, but internally options are tracked by
attribute names such as `cacheDir`.

## Desired behavior

Allow `Option.conflicts()` to accept long flag spellings and normalize them to
Commander option attribute names.

## Constraints

Existing attribute-name inputs must continue to work. The change should only
affect conflict declaration normalization.

## Success criteria

Declaring a conflict with `--cache-dir` behaves the same as declaring it with
`cacheDir`.
