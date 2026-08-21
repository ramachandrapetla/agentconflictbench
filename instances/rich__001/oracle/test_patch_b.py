from rich.text import Span, Text


def test_truncate_pad_preserves_existing_padding_contract() -> None:
    text = Text.from_markup("[red]x[/red]")

    text.truncate(3, pad=True)

    assert text.plain == "x  "
    assert len(text) == 3
    assert text.spans == [Span(0, 1, "red")]
