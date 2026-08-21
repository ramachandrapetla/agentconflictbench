# Task B: Delegate public Text.append(Text) to append_text

## Problem

Public `Text.append` and the internal `append_text` helper duplicate logic for
combining `Text` objects.

## Desired behavior

Refactor public `Text.append(Text)` to delegate to `append_text`.

## Constraints

The public `append` contract should remain unchanged, including preserving the
receiver's end metadata.

## Success criteria

Calling `text.append(other_text)` appends content and spans while keeping the
receiver's public metadata behavior stable.
