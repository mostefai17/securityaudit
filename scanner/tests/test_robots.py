import pytest
from unittest.mock import patch
from scanner.services.robots import check_robots


@patch('scanner.services.robots.requests.get')
def test_check_robots_success(mock_get):
    # Arrange: Setup mock response behavior
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = "User-agent: *\nDisallow:"

    # Act: Run the function
    result = check_robots("https://example.com/robots.txt")

    # Assert: Check the final output dictionary matches expectations
    assert result["exists"] is True
    assert result["status_code"] == 200
    assert result["is_valid_robots"] is True
