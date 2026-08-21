from rich.text import Span, Text


def test_public_append_does_not_inherit_appended_end_metadata() -> None:
    left = Text("left", end="!")
    right = Text("right", style="bold", end="?")

    left.append(right)

    assert left.plain == "leftright"
    assert left.spans == [Span(4, 9, "bold")]
    assert left.end == "!"
