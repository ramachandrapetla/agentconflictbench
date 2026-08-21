import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "src"))

from markupsafe import Markup, escape


def test_escape_soft_str_refactor_preserves_fallback_behavior() -> None:
    assert escape(Markup("<safe>")) == Markup("<safe>")
    assert escape(b"<x>") == Markup("b&#39;&lt;x&gt;&#39;")
