Prefer `__html_format__("")` when escaping HTML-aware objects.

Objects that implement both `__html__` and `__html_format__` should use the
format-aware method during plain escaping. This aligns direct escaping with the
formatting protocol used by `Markup.format()`.
