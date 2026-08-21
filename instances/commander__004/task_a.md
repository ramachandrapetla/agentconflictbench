Allow `Argument.argOptional()` to clear any default value when converting a
required positional argument into an optional argument.

This should prevent stale fallback values from remaining attached to arguments
whose required/optional status has changed after construction.
