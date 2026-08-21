from rich.text import Span, Text


def test_split_without_separator_preserves_spans() -> None:
    text = Text.from_markup("[red]x[/red]")

    (segment,) = text.split(",")

    assert segment.spans == [Span(0, 1, "red")]
