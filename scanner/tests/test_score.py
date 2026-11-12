from scanner.services.score import calculate_score


def test_calculate_score_unreachable_website():
    result = calculate_score(
        website={"reachable": False}, headers={}, ssl={}, robots={}, sitemap={}
    )
    assert result == {"grade": "F", "score": 0, "security percentage": "0.00%"}


def test_calculate_score_website_only():
    result = calculate_score(
        website={"reachable": True}, headers={}, ssl={}, robots={}, sitemap={}
    )
    assert result["score"] == 25
    assert result["grade"] == "E"


def test_calculate_score_full():
    result = calculate_score(
        website={"reachable": True},
        headers={"score": 7, "max_score": 7},
        ssl={"status": "valid"},
        robots={"is_valid_robots": True},
        sitemap={"is_valid_xml": True},
    )
    assert result["score"] == 90
    assert result["grade"] == "A+"
    assert result["security percentage"] == "90.00%"


def test_calculate_score_no_website():
    result = calculate_score(website=None, headers={}, ssl={}, robots={}, sitemap={})
    assert result["grade"] == "F"
    assert result["score"] == 0


def test_calculate_score_ssl_warning():
    result = calculate_score(
        website={"reachable": True},
        headers={},
        ssl={"status": "warning"},
        robots={},
        sitemap={},
    )
    assert result["score"] == 40
    assert result["grade"] == "D"
