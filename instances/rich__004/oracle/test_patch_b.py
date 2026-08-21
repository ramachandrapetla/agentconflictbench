from rich.text import Span, Text


def test_split_no_separator_refactor_preserves_copy_behavior() -> None:
    text = Text.from_markup("[red]x[/red]")

    (segment,) = text.split(",")

    assert segment.plain == "x"
    assert segment.spans == [Span(0, 1, "red")]
