Refactor set `.nonempty()` so it delegates to `.min(1)` instead of duplicating
minimum-size check construction.

The refactor should preserve other existing set cardinality constraints, such
as maximum size checks.
