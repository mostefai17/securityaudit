import requests
import requests.exceptions


def website_checking(url: str):

    results = {
        "is_https": url.startswith("https://"),
        "status_code": None,
        "reachable": False,
        "error": None,
        "final_url": None,
        "uses_https_after_redirect": False,
    }

    try:
        response = requests.get(
            url,
            timeout=5,
            allow_redirects=True,
        )

        results["status_code"] = response.status_code
        results["reachable"] = response.ok
        results["final_url"] = response.url
        results["uses_https_after_redirect"] = response.url.startswith("https://")

    except requests.exceptions.Timeout:
        results["error"] = "Website timed out"

    except requests.exceptions.RequestException as e:
        results["error"] = str(e)

    return results


def security_headers(url: str) -> dict:

    try:
        response = requests.get(url, timeout=5, allow_redirects=True)
    except requests.exceptions.RequestException as e:
        return {"error": f"failed to reach target: {e!s}"}

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
    content = {}

    for header in security_headers:
        if header in response.headers:
            content[header] = {"status": True, "value": response.headers[header]}
            score += 1
        else:
            content[header] = {"status": False, "value": None}

    return {"content": content, "score": (score / len(security_headers)) * 100}
