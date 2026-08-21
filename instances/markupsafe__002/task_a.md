Teach `soft_str()` to decode byte strings as UTF-8 text.

`soft_str()` is the helper for converting values to text without losing
`Markup` safety. Extend it so byte strings become decoded text instead of
Python's `b'...'` representation.
