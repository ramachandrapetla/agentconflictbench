# Task A: Case-insensitive QueryParams membership

## Problem

Some query parameter checks use membership tests, and callers may expect
parameter names to match regardless of casing.

## Desired behavior

Allow `QueryParams.__contains__` membership checks to treat parameter names
case-insensitively.

## Constraints

The change should only affect membership checks. Existing item access and
serialization behavior should remain unchanged unless explicitly updated.

## Success criteria

For query params containing `token=abc`, the expression `"TOKEN" in params`
returns true.
