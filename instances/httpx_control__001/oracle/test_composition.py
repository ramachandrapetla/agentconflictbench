import httpx


def test_header_and_query_helpers_compose_cleanly():
    headers = httpx.Headers([("X-Trace", "one"), ("x-trace", "two"), ("Other", "v")])
    params = httpx.QueryParams("a=1&a=2&empty=")

    assert headers.has_multiple("X-Trace") is True
    assert headers.has_multiple("Other") is False
    assert params.has_key("a") is True
    assert params.has_key("missing") is False
