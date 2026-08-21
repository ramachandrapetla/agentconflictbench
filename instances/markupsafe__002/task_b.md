Refactor `escape()` to use `soft_str()` for non-string fallback conversion.

The fallback branch of `escape()` currently calls `str()` directly. Delegate
that conversion to `soft_str()` so Markup-preserving string conversion behavior
is centralized.
