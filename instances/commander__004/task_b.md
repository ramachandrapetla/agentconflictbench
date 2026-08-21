# Task B: Accept prepared required arguments with defaults

## Problem

`Command.addArgument()` rejects a prepared required `Argument` that has a
default value, even though applications may want to interpret that default as a
fallback for omitted input.

## Desired behavior

Allow `Command.addArgument()` to treat such prepared arguments as optional
fallback arguments instead of throwing during registration.

## Constraints

The configured default should still be used when the argument is omitted.
Argument registration should continue to reject unrelated invalid argument
shapes.

## Success criteria

Adding `new Argument("<file>").default("fallback")` succeeds, and parsing with
no positional value passes `"fallback"` to the action.
