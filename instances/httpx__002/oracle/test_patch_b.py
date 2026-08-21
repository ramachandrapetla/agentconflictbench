import httpx


def test_loopback_alias_same_scheme_preserves_authorization():
    client = httpx.Client()
    request = client.build_request(
        "GET",
        "http://localhost:8000/start",
        headers={"Authorization": "Bearer secret"},
    )

    headers = client._redirect_headers(
        request,
        httpx.URL("http://127.0.0.1:8000/next"),
        "GET",
    )

    assert headers["Authorization"] == "Bearer secret"
