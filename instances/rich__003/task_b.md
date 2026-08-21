Refactor `Text.copy()` through existing copy helpers.

Replace the duplicated metadata construction in `copy()` with `blank_copy()`,
then copy inline spans via `copy_styles()`. The public `copy()` result should be
unchanged.
