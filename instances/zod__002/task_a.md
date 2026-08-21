When changing the catchall policy for an object schema, clear any existing
object-level refinements so the catchall variant can be validated independently.

The new catchall schema should still accept unknown keys according to the
provided catchall type.
