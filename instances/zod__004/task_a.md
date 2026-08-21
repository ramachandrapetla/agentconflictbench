When applying a new minimum size to a set schema, replace any existing set-size
checks so the new lower-bound policy is evaluated independently.

The resulting schema should still enforce the newly requested minimum size.
