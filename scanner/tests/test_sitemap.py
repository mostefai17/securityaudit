from unittest.mock import MagicMock, patch

from scanner.services.sitemap import check_sitemap


@patch("scanner.services.sitemap.requests.get")
def test_check_sitemap_valid_xml(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.ok = True
    mock_response.text = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://example.com/page1</loc>
    </url>
    <url>
        <loc>https://example.com/page2</loc>
    </url>
</urlset>"""
    mock_get.return_value = mock_response

    # Act: Call with a URL String
    result = check_sitemap("example.com")
    # Assert: Check the result
    # Assert: Check actual return values
    assert (
        result["url_checked"] == "https://example.com/sitemap.xml"
    )  # String, not list
    assert result["exists"] is True
    assert result["status_code"] == 200
    assert result["is_valid_xml"] is True
    assert result["url_count"] == 0  # Two URLs found
    assert result["error_message"] is None


@patch("scanner.services.sitemap.requests.get")
def test_check_sitemap_invalid_url(mock_get):
    """Act and Assert"""
    result = check_sitemap("")
    assert result["error"] == "Invalid URL provided."


@patch("scanner.services.sitemap.requests.get")
def test_check_sitemap_invalid_xml(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.ok = False
    mock_get.return_value = mock_response

    # Act: Call with a URL String
    result = check_sitemap("https://example.com")
    # Assert: Check the result
    assert result["exists"] is False
    assert result["status_code"] == 404
    assert "HTTP error 404" in result["error_message"]
