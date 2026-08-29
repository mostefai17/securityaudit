import pytest
import requests_mock
from scanner.services.score import calculate_score

def test_calculate_score():
    headers = "value"
    ssl = "value"
    robots = "value"
    sitemap = "value"
    website = "value"

    if website == "value" and headers == "value" and ssl == "value" and robots == "value" and sitemap == "value":
        score = calculate_score(website, headers, ssl, robots, sitemap)
        assert score["score"] == 0
    elif not website:
        assert calculate_score(website, headers, ssl, robots, sitemap) == {"grade": "F", "score": 0, "security percentage": "0.00%"}
    else:
        assert calculate_score(website, headers, ssl, robots, sitemap) == {"error": "No response received from the server."}
