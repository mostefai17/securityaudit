def calculate_score(website, headers, ssl, robots, sitemap):
    score = 0
    max_score = 100

    if not website or not isinstance(website, dict) or not website.get("reachable"):
        return {"grade": "F", "score": 0, "security_percentage": "0.00%"}

    score += 25

    if headers and isinstance(headers, dict):
        header_score = headers.get("score")
        max_header_score = headers.get("max_score")
        if header_score is not None and max_header_score:
            score += 20

    if ssl and isinstance(ssl, dict):
        if ssl.get("status") in ("valid", "warning"):
            score += 15

    if robots and isinstance(robots, dict):
        if robots.get("is_valid_robots"):
            score += 15

    if sitemap and isinstance(sitemap, dict):
        if sitemap.get("is_valid_xml"):
            score += 15

    if score >= 90:
        grade = "A+"
    elif score >= 80:
        grade = "A"
    elif score >= 70:
        grade = "B"
    elif score >= 55:
        grade = "C"
    elif score >= 40:
        grade = "D"
    elif score >= 25:
        grade = "E"
    else:
        grade = "F"

    return {
        "grade": grade,
        "score": score,
        "security_percentage": f"{score / max_score * 100:.2f}%",
    }
