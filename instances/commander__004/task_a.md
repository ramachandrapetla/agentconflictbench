# Task A: Clear defaults when making prepared arguments optional

## Problem

A prepared `Argument` can be converted from required to optional after it has
already been given a default value, leaving stale fallback state attached to the
argument.

## Desired behavior

Update `Argument.argOptional()` so converting an argument to optional clears any
existing default value.

## Constraints

The method should still mark the argument optional and return the argument for
chaining. Other argument metadata should remain unchanged.

## Success criteria

Calling `new Argument("<file>").default("fallback").argOptional()` produces an
optional argument whose default value is unset.
