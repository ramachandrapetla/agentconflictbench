# Task B: Optional wrappers inherit descriptive metadata

## Problem

Optional wrapper schemas can lose descriptive metadata from their inner schema,
making generated documentation less useful.

## Desired behavior

Make optional wrappers inherit descriptive metadata from the inner schema.

## Constraints

Registration IDs should not be inherited into wrapper schemas. The wrapper
should remain distinguishable from the inner schema for identity-sensitive
metadata.

## Success criteria

`z.string().describe("Name").optional()` exposes the description, while wrapper
metadata does not inherit the inner schema's registration ID.
