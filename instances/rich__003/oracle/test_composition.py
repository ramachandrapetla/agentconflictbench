from rich.text import Span, Text


def test_copy_does_not_duplicate_spans() -> None:
    text = Text.from_markup("[red]x[/red]")

    copy = text.copy()

    assert copy.spans == [Span(0, 1, "red")]
