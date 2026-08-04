

def calculate_score(website,headers,ssl,robots,sitemap):
    score = 0
    max_score = 100

    try:
        if website["reachable"] is None:
            return {"grade": "N/A", "score": 0, "security percentage": "N/A"}
    except Exception as e:
        return {"error": f"Error calculating score: {e}"}

    if website and website.get("reachable"):
        score += 25

    if headers and headers.get("score") is not None and headers.get("max_score"):
        score += 20

    if ssl and ssl.get("status") == "valid":
        score += 20

    if robots and robots.get("is_valid_robots") == True:
        score += 15

    if sitemap and sitemap.get("is_valid_xml") == True:
        score += 15


    if score >= 90:
        return {
            "grade": "A+",
            "score": score,
            "security percentage": f"{score/max_score*100:.2f}%"
        }

    elif score >= 80:
        return {
            "grade": "A",
            "score": score,
            "security percentage": f"{score/max_score*100:.2f}%"
        }

    elif score >= 70:
        return {
            "grade": "B",
            "score": score,
            "security percentage": f"{score/max_score*100:.2f}%"
        }

    elif score >= 55:
        return {
            "grade": "C",
            "score": score,
            "security percentage": f"{score/max_score*100:.2f}%"
        }

    elif score >= 40:
        return {
            "grade": "D",
            "score": score,
            "security percentage": f"{score/max_score*100:.2f}%"
        }

    elif score >= 25:
        return {
            "grade": "E",
            "score": score,
            "security percentage": f"{score/max_score*100:.2f}%"
        }

    else:
        return {
            "grade": "F",
            "score": score,
            "security percentage": f"{score/max_score*100:.2f}%"
        }