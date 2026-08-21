Return metadata-only text when `divide()` is called with no offsets.

For callers using `divide()` as a segmentation primitive, an empty offset list
should produce one plain segment that preserves Text metadata but does not carry
inline spans from the original text.
