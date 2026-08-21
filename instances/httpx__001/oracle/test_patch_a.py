import httpx


def test_queryparams_contains_is_case_insensitive():
    params = httpx.QueryParams({"Token": "abc"})

    assert "token" in params
    assert "TOKEN" in params
