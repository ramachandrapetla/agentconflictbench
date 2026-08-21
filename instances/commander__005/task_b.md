Simplify option value handling by resolving boolean and optional options before
the dedicated negated-option branch.

The behavior of `--no-*` options without explicit values should remain
unchanged: passing the flag should set the option value to `false`.
