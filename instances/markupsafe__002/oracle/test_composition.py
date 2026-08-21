import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "src"))

from markupsafe import Markup, escape


def test_escape_bytes_keeps_python_bytes_representation() -> None:
    assert escape(b"<x>") == Markup("b&#39;&lt;x&gt;&#39;")
