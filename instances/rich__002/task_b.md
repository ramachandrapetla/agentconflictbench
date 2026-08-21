Refactor public `Text.append(Text)` to reuse `append_text()`.

The public append path currently duplicates the span-copying logic already
implemented by `append_text()`. Delegate the `Text` case to that helper while
preserving the public `append()` API contract.
