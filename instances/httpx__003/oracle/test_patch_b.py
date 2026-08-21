import httpx


def test_update_replaces_existing_logical_header():
    headers = httpx.Headers({"X-Token": "old"})

    headers.update({"x-token": "new"})

    assert headers.get_list("x-token") == ["new"]
