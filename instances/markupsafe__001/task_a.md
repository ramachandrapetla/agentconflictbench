Make old-style `Markup` formatting treat `None` as an empty optional value.

When `%s` formatting receives `None`, the old-style escape helper should use
the silent escaping path so optional template values render as empty strings
instead of the literal text `None`.
