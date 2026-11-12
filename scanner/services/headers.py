# scanner/services/headers.py


def security_headers(response) -> dict:

    security_headers = [
        "X-Frame-Options",
        "X-XSS-Protection",
        "X-Content-Type-Options",
        "Content-Security-Policy",
        "Strict-Transport-Security",
        "Referrer-Policy",
        "Permissions-Policy",
    ]

    score = 0
    findings = {}

    if response is None:
        for header in security_headers:
            findings[header] = {
                "present": False,
                "value": None,
            }

        return {
            "headers": findings,
            "score": 0,
            "max_score": len(security_headers),
            "error": "No response received from the server.",
        }

    for header in security_headers:
        if header in response.headers:
            findings[header] = {
                "present": True,
                "value": response.headers[header],
            }

            score += 1

        else:
            findings[header] = {
                "present": False,
                "value": None,
            }

    return {
        "headers": findings,
        "score": score,
        "max_score": len(security_headers),
    }
