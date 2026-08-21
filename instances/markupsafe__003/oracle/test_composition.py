import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "src"))

from markupsafe import Markup


class HTMLAndFormat:
    def __html__(self) -> str:
        return "<html>"

    def __html_format__(self, format_spec: str) -> str:
        return "<format>"


def test_markup_constructor_still_uses_html_method_for_html_aware_objects() -> None:
    assert Markup(HTMLAndFormat()) == Markup("<html>")
