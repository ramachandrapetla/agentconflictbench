Reuse the old-style escape helper for simple `Markup.format()` fields.

For replacement fields without a format specifier, route new-style formatting
through the same helper used by `%` formatting. This keeps escaping behavior
centralized while preserving existing `format()` behavior.
