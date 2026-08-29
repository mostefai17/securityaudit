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




