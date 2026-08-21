import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "src"))

from markupsafe import Markup


def test_simple_format_fields_preserve_existing_escape_behavior() -> None:
    assert Markup("<{}>").format("<x>") == Markup("<&lt;x&gt;>")
    assert Markup("{}").format(None) == Markup("None")
    assert Markup("{:.2f}").format(1.234) == Markup("1.23")
