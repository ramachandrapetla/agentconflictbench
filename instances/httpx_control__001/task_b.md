# Patch B task

Add a helper for query-parameter key presence.

Callers that inspect query strings need a direct way to ask whether a key is
present without retrieving a value. Add `QueryParams.has_key(key)` that returns
whether the normalized key exists in the query parameter mapping.

Constraints:

- Do not change query-parameter parsing.
- Do not change `QueryParams.get()` or `QueryParams.get_list()`.
- Preserve support for non-string keys by normalizing through `str(key)`.
