import pytest
import requests_mock
from scanner.services.score import calculate_score

def test_calculate_score():
    headers = "value"
    ssl = "value"
    robots = "value"
    sitemap = "value"
    website = "value"

    assert calculate_score(headers, ssl, robots, sitemap,website) == {'grade': 'F', 'score': 0, 'security percentage': '0.00%'}

