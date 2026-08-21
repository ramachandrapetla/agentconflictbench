import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "src"))

from markupsafe import escape, soft_str


def test_soft_str_decodes_bytes_without_changing_escape_bytes_contract() -> None:
    assert soft_str(b"<x>") == "<x>"
    assert escape(b"<x>") == "b&#39;&lt;x&gt;&#39;"
