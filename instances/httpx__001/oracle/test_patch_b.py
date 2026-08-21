import httpx


def test_queryparams_get_still_returns_exact_key_value():
    params = httpx.QueryParams({"token": "abc"})

    assert params.get("token") == "abc"
    assert params.get("missing", "fallback") == "fallback"
