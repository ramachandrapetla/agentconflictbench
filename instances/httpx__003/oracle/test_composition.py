import httpx


def test_update_preserves_single_logical_header_after_case_change():
    headers = httpx.Headers({"x-token": "old"})

    headers.update({"X-Token": "new"})

    assert headers.get_list("x-token") == ["new"]
