Delegate `Markup` construction for HTML-aware objects through `escape()`.

`Markup.__new__()` currently calls `__html__()` directly. Route HTML-aware
objects through the central `escape()` helper so construction and direct escape
share safety handling.
