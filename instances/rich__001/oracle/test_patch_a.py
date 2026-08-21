from rich.text import Span, Text


def test_pad_right_extends_trailing_inline_style_over_padding() -> None:
    text = Text.from_markup("[red]x[/red]")

    text.pad_right(2)

    assert text.plain == "x  "
    assert text.spans == [Span(0, 3, "red")]
