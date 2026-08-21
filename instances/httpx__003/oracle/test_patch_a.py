import httpx


def test_headers_keys_preserve_original_casing():
    headers = httpx.Headers([("X-Token", "one")])

    assert list(headers.keys()) == ["X-Token"]
