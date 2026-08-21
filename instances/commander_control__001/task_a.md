# Patch A task

Add an introspection helper for positional arguments.

Users who build higher-level tooling around Commander need to know whether an
`Argument` instance is required without parsing the decorated usage string. Add
an `isRequired()` method to `Argument` that returns the argument's existing
required/optional state.

Constraints:

- Do not change parsing behavior.
- Do not change argument construction or help output.
- Preserve the existing `argOptional()` behavior.
