import httpx


def test_case_insensitive_contains_does_not_break_get_default():
    params = httpx.QueryParams({"Token": "abc"})

    assert params.get("token", "missing") == "missing"
