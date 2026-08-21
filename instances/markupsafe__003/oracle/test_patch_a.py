import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "src"))

from markupsafe import Markup, escape


class HTMLAndFormat:
    def __html__(self) -> str:
        return "<html>"

    def __html_format__(self, format_spec: str) -> str:
        assert format_spec == ""
        return "<format>"


def test_escape_prefers_empty_html_format_without_changing_markup_constructor() -> None:
    value = HTMLAndFormat()

    assert escape(value) == Markup("<format>")
    assert Markup(value) == Markup("<html>")
