Use the existing padding helper when `Text.truncate(..., pad=True)` adds spaces.

The truncation path currently appends padding manually. Refactor the short-text
padding case to delegate to `pad_right()` so length bookkeeping and future
padding behavior remain centralized.
