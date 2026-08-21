# Patch B task

Add number-format introspection for integer schemas.

Tooling that inspects numeric Zod schemas needs to know whether a schema is an
integer schema without parsing internals directly. Add an `isIntegerFormat()`
helper to number schemas that returns the existing integer flag.

Constraints:

- Do not change number validation behavior.
- Do not change how integer schemas are constructed.
- Preserve existing number refinement methods.
