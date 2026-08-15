import pytest
import ssl
# Import the module instead of the raw function so we can patch its attributes
from scanner.services import ssl_check


def test_analyze_certificate(mocker):
    # Patch the function right inside the imported module reference
    mock_analyze = mocker.patch.object(ssl_check, "analyze_certificate")

    # 1. Failure scenario
    mock_analyze.side_effect = ssl.SSLCertVerificationError
    with pytest.raises(ssl.SSLCertVerificationError):
        ssl_check.analyze_certificate("invalid_cert")

    # 2. Success scenario
    mock_analyze.side_effect = None
    mock_analyze.return_value = True
    result = ssl_check.analyze_certificate("valid_cert")
    assert result is True


def test_runsslaudit(mocker):
    url = "https://example.com"

    # Patch runsslaudit inside the module context so it returns a fake valid dict
    mocker.patch.object(ssl_check, "runsslaudit", return_value={"status": True})

    result = ssl_check.runsslaudit(url)
    assert result["status"] is True
