from unittest.mock import MagicMock

from scanner.services.headers import security_headers


def test_security_headers_all_present():
    mock_response = MagicMock()
    mock_response.headers = {
        "X-Frame-Options": "SAMEORIGIN",
        "X-XSS-Protection": "1; mode=block",
        "X-Content-Type-Options": "nosniff",
        "Content-Security-Policy": "default-src 'self'; script-src 'self'",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains; preload",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "Permissions-Policy": "geolocation=()",
    }
    # Act
    result = security_headers(response=mock_response)
    # Assert
    assert isinstance(result["headers"], dict)
    assert result["score"] == 7
    assert result["max_score"] == 7
    for header in result["headers"].values():
        assert header["present"] is True


def test_security_headers_none_present():
    mock_response = MagicMock()
    mock_response.headers = {}

    result = security_headers(response=mock_response)

    assert result["score"] == 0
    assert result["max_score"] == 7
    for header in result["headers"].values():
        assert header["present"] is False


def test_security_headers_no_response():
    result = security_headers(response=None)

    assert result["score"] == 0
    assert result["error"] == "No response received from the server."
    assert result["max_score"] == 7
