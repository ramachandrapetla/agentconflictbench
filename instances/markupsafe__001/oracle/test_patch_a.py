import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "src"))

from markupsafe import Markup


def test_old_style_markup_formatting_treats_none_as_empty() -> None:
    assert Markup("%s") % None == Markup("")
    assert Markup("{}").format(None) == Markup("None")
