from rich.text import Span, Text


def test_truncate_padding_does_not_inherit_content_style() -> None:
    text = Text.from_markup("[red]x[/red]")

    text.truncate(3, pad=True)

    assert text.plain == "x  "
    assert text.spans == [Span(0, 1, "red")]
