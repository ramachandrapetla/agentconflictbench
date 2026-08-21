# Task B: Lowercase fallback for Click command lookup

## Problem

Command invocations with accidental uppercase spelling fail even when the
registered command has a clear lowercase equivalent.

## Desired behavior

When exact lookup fails, retry lookup using the lowercase form of the invoked
command name.

## Constraints

Exact matches must still take priority. The fallback should not make command
registration case-insensitive globally.

## Success criteria

A group containing `status` can resolve `STATUS` to `status` when no exact
`STATUS` command exists.
