Refactor array `.nonempty()` so it delegates to `.min(1)` instead of duplicating
minimum-length check construction.

The refactor should preserve other existing array cardinality constraints, such
as maximum length checks.
