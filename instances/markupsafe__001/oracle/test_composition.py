import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "src"))

from markupsafe import Markup


def test_new_style_formatting_does_not_silently_drop_none() -> None:
    assert Markup("{}").format(None) == Markup("None")
