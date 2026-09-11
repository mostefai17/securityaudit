import pytest
from scanner.services.website import website_check
from unittest.mock import MagicMock


def test_website_check():
    mock_response = MagicMock()
    mock_response.ok = True
    mock_response.status_code = 200
    mock_response.url = "https://example.com"

    result = website_check("https://example.com", response=mock_response)

    assert result["reachable"] is True
    assert result["status_code"] == 200
    assert result["is_https"] is True
    assert result["final_url"] == "https://example.com"


def test_website_check_no_response():
    result = website_check("https://example.com", response=None)

    assert result["reachable"] is False
    assert result["status_code"] is None
    assert result["error"] == "There is no response"


def test_website_check_http_url():
    mock_response = MagicMock()
    mock_response.ok = True
    mock_response.status_code = 200
    mock_response.url = "http://example.com"

    result = website_check("http://example.com", response=mock_response)

    assert result["is_https"] is False
    assert result["uses_https_after_redirect"] is False


def test_website_check_redirected_to_https():
    mock_response = MagicMock()
    mock_response.ok = True
    mock_response.status_code = 200
    mock_response.url = "https://example.com"

    result = website_check("http://example.com", response=mock_response)

    assert result["is_https"] is False
    assert result["uses_https_after_redirect"] is True


def test_website_check_not_reachable():
    mock_response = MagicMock()
    mock_response.ok = False
    mock_response.status_code = 503
    mock_response.url = "https://example.com"

    result = website_check("https://example.com", response=mock_response)
    # Assert
    assert result["reachable"] is False
    assert result["status_code"] == 503




