from rich.text import Span, Text


def test_copy_helper_refactor_preserves_spans_once() -> None:
    text = Text.from_markup("[red]x[/red]")

    copy = text.copy()

    assert copy is not text
    assert copy.plain == "x"
    assert copy.spans == [Span(0, 1, "red")]
