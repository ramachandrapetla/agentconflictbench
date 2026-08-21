# Task B: Lowercase fallback for Typer invocations

## Problem

Case mistakes in command invocations are common, especially in scripts and
documentation examples.

## Desired behavior

When exact Typer command lookup fails, retry lookup using the lowercase invoked
name.

## Constraints

The fallback should not rewrite registered command names or affect exact
case-sensitive matches.

## Success criteria

A command registered as `status` can be invoked as `STATUS` when no exact
uppercase command exists.
