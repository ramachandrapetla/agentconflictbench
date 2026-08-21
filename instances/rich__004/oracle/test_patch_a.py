from rich.text import Text


def test_divide_without_offsets_returns_metadata_only_segment() -> None:
    text = Text.from_markup("[red]x[/red]", justify="center")

    (segment,) = text.divide([])

    assert segment.plain == "x"
    assert segment.justify == "center"
    assert segment.spans == []
