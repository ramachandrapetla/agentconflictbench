# Patch B task

Add an introspection helper for negated options.

Users who inspect command schemas need to distinguish `--no-*` options from
ordinary boolean options without reaching into private fields. Add an
`isNegated()` method to `Option` that returns whether the option was declared as
a negated option.

Constraints:

- Do not change option parsing behavior.
- Do not change how boolean options are classified.
- Preserve existing negated option semantics.
