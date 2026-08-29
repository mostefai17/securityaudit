import pytest
from unittest.mock import MagicMock
from scanner.services.audit import run_security_audit

def test_run_security_audit(mocker):
    url = "https://example.com"

    # Mocking the audit level
    mocker.patch("scanner.services.audit.check_sitemap", return_value={"sitemap": True})
    mocker.patch("scanner.services.audit.runsslaudit", return_value={"ssl": True})
    mocker.patch("scanner.services.audit.website_check", return_value={"website":True})
    #Act
    audit_results = run_security_audit(url)
    #Assert
    assert audit_results["url"] == url + "/"
    # assert audit_results["audit_results"] == {
    #     "website": { "reachable": True, "status_code": 200, "is_https": True, "final_url": url },
    # }
    assert audit_results["status_code"] == None
    assert audit_results["url_final_boss"] == url + "/"