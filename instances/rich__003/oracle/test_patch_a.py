from rich.text import Span, Text


def test_blank_copy_with_plain_preserves_spans() -> None:
    text = Text.from_markup("[red]x[/red]")

    copy = text.blank_copy(text.plain)

    assert copy.plain == "x"
    assert copy.spans == [Span(0, 1, "red")]
    assert text.copy().spans == [Span(0, 1, "red")]
