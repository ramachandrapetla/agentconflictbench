import httpx


def test_headers_has_multiple_detects_repeated_values():
    headers = httpx.Headers([("X-Trace", "one"), ("x-trace", "two"), ("Other", "v")])

    assert headers.has_multiple("X-Trace") is True
    assert headers.has_multiple("x-trace") is True
    assert headers.has_multiple("Other") is False
    assert headers.has_multiple("Missing") is False
