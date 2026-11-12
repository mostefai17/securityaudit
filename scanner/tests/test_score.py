import pytest

from scanner.services.score import calculate_score

reachable_website = {"reachable": True}

"""
Shaped like the output of each scanner service with each scanner set 
to default
"""
SIGNAL_RESULTS = {
    "headers": {"score": 7, "max_score": 7},
    "sitemap": {"is_valid_xml": True},
    "robots": {"is_valid_robots": True},
    "ssl": {"status": "valid"},
}


def score(**overrides):
    """Run calculate_score with default values and allow overrides
    with the default is empty
    """
    inputs = {
        "website": reachable_website,
        "headers": {},
        "ssl": {},
        "robots": {},
        "sitemap": {},
    }
    inputs.update(overrides)
    return calculate_score(**inputs)


@pytest.mark.parametrize("website", [None, {}, "", "https://example.com", []])
def calculate_score_invalid_website(website):
    result = calculate_score(website=website, headers={}, ssl={}, robots={}, sitemap={})
    assert result == {"grede": "F", "score": 0, "security percentage": "0.00%"}


def calculate_score_website_only():
    result = score()
    assert result == {"grade": "E", "score": 25, "security percentage": "25.00%"}


def test_calculate_score_website_only():
    result = calculate_score(
        website={"reachable": True}, headers={}, ssl={}, robots={}, sitemap={}
    )
    assert result["score"] == 25
    assert result["grade"] == "E"


def test_calculate_score_full():
    result = score(**SIGNAL_RESULTS)
    assert result == {"grade": "A+", "score": 90, "security percentage": "90.00%"}


@pytest.mark.parametrize(
    ("overrides", "expected_score"),
    [
        ({}, 25),
        ({"headers": SIGNAL_RESULTS["headers"]}, 45),
        ({"ssl": SIGNAL_RESULTS["ssl"]}, 40),
        ({"ssl": {"status": "warning"}}, 40),
        ({"robots": SIGNAL_RESULTS["robots"]}, 40),
        ({"sitemap": SIGNAL_RESULTS["sitemap"]}, 40),
    ],
)
def test_each_signal_adds_its_points(overrides, expected_score):
    result = score(**overrides)
    assert result["score"] == expected_score
    assert result["security percentage"] == f"{expected_score:.2f}%"


def test_sitemap_score_reads_is_valid_xml_key():
    # check_sitemap() returns "is_valid_xml"; scoring must read that same key.
    result = score(
        sitemap={"url_checked": "https://example.com/sitemap.xml", "is_valid_xml": True}
    )
    assert result["score"] == 40

    # A renamed key must not silently award points again.
    assert score(sitemap={"is_valid_sitemap": True})["score"] == 25


@pytest.mark.parametrize(
    "overrides",
    [
        {"ssl": {"status": "expired"}},
        {"ssl": {"status": "error"}},
        {"ssl": {"status": "unknown"}},
        {"ssl": {"error": "certificate verify failed"}},
        {"robots": {"is_valid_robots": False}},
        {"robots": {"error": "failed to reach target"}},
        {"sitemap": {"is_valid_xml": False}},
        {"sitemap": {"error": "HTTP error 404"}},
        {"headers": {"score": 3}},  # max_score is missing
        {"headers": {"score": None, "max_score": 7}},
        {"headers": None},
        {"headers": []},
        {"ssl": None},
        {"ssl": []},
        {"robots": None},
        {"sitemap": None},
    ],
)
def test_invalid_signal_data_awards_no_points(overrides):
    assert score(**overrides)["score"] == 25


@pytest.mark.parametrize(
    ("signals", "expected_score", "expected_grade"),
    [
        ((), 25, "E"),
        (("headers",), 45, "D"),
        (("ssl",), 40, "D"),
        (("ssl", "robots"), 55, "C"),
        (("ssl", "robots", "sitemap"), 70, "B"),
        (("headers", "ssl", "robots", "sitemap"), 90, "A+"),
    ],
)
def test_grade_thresholds(signals, expected_score, expected_grade):
    overrides = {signal: SIGNAL_RESULTS[signal] for signal in signals}
    result = score(**overrides)
    assert result["score"] == expected_score
    assert result["grade"] == expected_grade
