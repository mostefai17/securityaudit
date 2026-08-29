import pytest
from unittest.mock import MagicMock
from scanner.services.headers import security_headers

def test_security_headers():
    mock_response = MagicMock()
    mock_response.headers = {
        "X-Frame-Options": "SAMEORIGIN",
        "X-XSS-Protection": "1; mode=block",
        "X-Content-Type-Options": "nosniff",
        "Content-Security-Policy": "default-src 'self'; script-src 'self'",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains; preload",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "Permissions-Policy": "geolocation=()",
        "X-Permitted-Cross-Domain-Policies": "none",
        "X-Download-Options": "noopen",
    }
    # Act
    respone = security_headers(response=mock_response)
    # Assert
    assert respone["headers"] == True
    assert respone["score"] == 10
    assert respone["max_score"] == 10
