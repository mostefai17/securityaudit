

def calculate_score(website,headers,ssl,robots,sitemap):
    score = 0
    max_score = 100

    if website["reachable"]:
        score += 25

    if headers["headers"]:
        score += 20

    if ssl["status"]:
        score += 25

    if robots["status_code"] == 200:
        score += 15

    if sitemap["status_code"] == 200:
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