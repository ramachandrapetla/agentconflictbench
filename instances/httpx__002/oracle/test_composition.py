import httpx


def test_loopback_alias_https_upgrade_strips_authorization():
    client = httpx.Client()
    request = client.build_request(
        "GET",
        "http://localhost:8000/start",
        headers={"Authorization": "Bearer secret"},
    )

    headers = client._redirect_headers(
        request,
        httpx.URL("https://127.0.0.1:8000/secure"),
        "GET",
    )

    assert "Authorization" not in headers
