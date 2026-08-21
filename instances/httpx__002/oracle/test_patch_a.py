import httpx


def test_loopback_https_upgrade_preserves_authorization():
    client = httpx.Client()
    request = client.build_request(
        "GET",
        "http://localhost:8000/start",
        headers={"Authorization": "Bearer secret"},
    )

    headers = client._redirect_headers(
        request,
        httpx.URL("https://localhost:8000/secure"),
        "GET",
    )

    assert headers["Authorization"] == "Bearer secret"
