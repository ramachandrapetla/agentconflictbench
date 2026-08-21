Preserve appended `Text.end` metadata in the low-level append helper.

When `append_text()` combines two `Text` objects, it should also copy the
appended object's `end` value. This lets callers that deliberately use the
lower-level helper keep both content and trailing line-ending metadata together.
