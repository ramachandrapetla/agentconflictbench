# Task A: Decode bytes in soft_str

## Problem

`soft_str` is used as a gentle conversion helper, but byte strings are displayed
as Python bytes representations instead of decoded text.

## Desired behavior

Teach `soft_str` to decode byte strings as UTF-8 text.

## Constraints

Existing string and Markup inputs should continue to pass through as before.
The decoding behavior should be limited to byte-like inputs.

## Success criteria

Calling `soft_str(b"caf\\xc3\\xa9")` returns `"café"`.
