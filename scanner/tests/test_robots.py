import pytest
from unittest.mock import patch
import requests
from scanner.services.robots import check_robots


@patch('scanner.services.robots.requests.get')
def test_check_robots_success(mock_get):
    # Arrange: Setup mock response behavior
    mock_get.return_value.status_code = 200
    mock_get.return_value.ok = True
    mock_get.return_value.text = "User-agent: *\nDisallow:"

    # Act: Run the function
    result = check_robots("https://example.com/robots.txt")

    # Assert: Check the final output dictionary matches expectations
    assert result["exists"] is True
    assert result["status_code"] == 200
    assert result["is_valid_robots"] is True


@patch('scanner.services.robots.requests.get')
def test_check_robots_not_found(mock_get):
    mock_get.return_value.status_code = 404
    mock_get.return_value.ok = False

    result = check_robots("https://example.com")

    assert result["exists"] is False
    assert result["is_valid_robots"] is False
    assert "404" in result["error_message"]


@patch('scanner.services.robots.requests.get')
def test_check_robots_network_error(mock_get):
    mock_get.side_effect = requests.RequestException("Connection refused")

    result = check_robots("https://example.com")

    assert "error" in result
    assert "failed to reach target" in result["error"]


def test_check_robots_invalid_url():
    result = check_robots("")

    assert "error" in result
