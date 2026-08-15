import pytest
from unittest.mock import MagicMock
from scanner.services.audit import run_security_audit

def test_run_security_audit(mocker):
    url = "https://example.com"

    # Mocking the audit level
    mocker.patch("scanner.services.audit.check_sitemap", return_value={"sitemap": True})
    mocker.patch("scanner.services.audit.runsslaudit", return_value={"ssl": True})
    mocker.patch("scanner.services.audit.website_check", return_value={"website":True})

    result = run_security_audit(url)
    assert result["audit_results"]["website"] is not None