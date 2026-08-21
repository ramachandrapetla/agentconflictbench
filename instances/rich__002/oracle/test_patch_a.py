from rich.text import Text


def test_append_text_inherits_appended_end_metadata() -> None:
    left = Text("left", end="\n")
    right = Text("right", end="")

    left.append_text(right)

    assert left.plain == "leftright"
    assert left.end == ""
