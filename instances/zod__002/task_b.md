Refactor `.loose()` so it delegates to `.catchall(z.unknown())` instead of
duplicating the object cloning logic.

The refactor should preserve existing object-level refinements when converting
an object schema to loose mode.
