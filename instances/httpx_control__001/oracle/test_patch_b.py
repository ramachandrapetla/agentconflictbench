import httpx


def test_query_params_has_key_detects_presence():
    params = httpx.QueryParams("a=1&a=2&empty=")

    assert params.has_key("a") is True
    assert params.has_key("empty") is True
    assert params.has_key("missing") is False
    assert params.has_key(123) is False
