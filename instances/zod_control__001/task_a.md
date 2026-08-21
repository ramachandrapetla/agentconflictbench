# Patch A task

Add string-format introspection for email schemas.

Tooling that receives a Zod string schema needs to know whether the schema was
created with the email format without parsing internals directly. Add an
`isEmailFormat()` helper to string schemas that returns whether the schema's
format is `email`.

Constraints:

- Do not change string validation behavior.
- Do not change how email schemas are constructed.
- Preserve existing string format methods.
