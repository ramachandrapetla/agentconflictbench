When applying a new minimum length to an array schema, replace any existing
array-length checks so the new lower-bound policy is evaluated independently.

The resulting schema should still enforce the newly requested minimum length.
