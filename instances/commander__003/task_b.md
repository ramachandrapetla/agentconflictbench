# Task B: Flag spelling aliases for implied option values

## Problem

Commander implication declarations are easier to read when they use CLI flag
spellings, but implied values are applied using internal option attribute names.

## Desired behavior

Allow `Option.implies()` to accept long flag spellings and normalize them when
setting implied option values.

## Constraints

Existing attribute-name inputs must continue to work. The change should not
alter how users provide options on the command line.

## Success criteria

An implication declared for `--cache-dir` sets the same option value as an
implication declared for `cacheDir`.
