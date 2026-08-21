Allow `blank_copy()` to copy spans when a replacement plain string is provided.

`blank_copy()` already preserves metadata such as style, wrapping, end, and tab
size. When callers provide replacement plain text, also preserve existing spans
so helper-based copies can keep inline style ranges.
