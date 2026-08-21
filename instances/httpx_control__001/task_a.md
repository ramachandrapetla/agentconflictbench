# Patch A task

Add a helper for detecting repeated header values.

Consumers that inspect HTTP response metadata sometimes need to know whether a
header was provided more than once without manually calling and counting
`get_list()`. Add `Headers.has_multiple(key)` that returns `True` when the
header has multiple stored values.

Constraints:

- Do not change header lookup or normalization behavior.
- Preserve existing `Headers.get()` and `Headers.get_list()` behavior.
- The helper should be case-insensitive like other header accessors.
