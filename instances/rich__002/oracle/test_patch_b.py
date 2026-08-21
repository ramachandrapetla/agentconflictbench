from rich.text import Span, Text


def test_public_append_text_refactor_preserves_receiver_end() -> None:
    left = Text("left", end="!")
    right = Text("right", style="bold", end="?")

    left.append(right)

    assert left.plain == "leftright"
    assert left.spans == [Span(4, 9, "bold")]
    assert left.end == "!"
