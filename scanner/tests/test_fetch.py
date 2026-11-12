from scanner.services.fetch import fetch


def test_fetch(requests_mock):
    url = "https://example.com"
    mocked_html = "<html><body><h1>Example Domain</h1></body></html>"

    requests_mock.get(url, text=mocked_html, status_code=200)
    result = fetch(url)

    assert result.text == mocked_html


def test_fetch_failure(requests_mock):
    import requests

    url = "https://unreachable.example.com"
    requests_mock.get(url, exc=requests.exceptions.ConnectionError)

    result = fetch(url)

    assert result is None
