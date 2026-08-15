# scanner/services/website.py

import requests


def website_check(url: str, response) -> dict:
    """
    Basic website information.
    """

    results = {
        "reachable": False,
        "status_code": None,
        "is_https": url.startswith("https://"),
        "final_url": None,
        "uses_https_after_redirect": False,
    }
    if response is None:
        results["error"] = "There is no response"
        return results

    try:
        results["reachable"] = response is True
        results["status_code"] = response.status_code
        results["final_url"] = response.url
        results["uses_https_after_redirect"] = response.url.startswith("https://")

    except requests.exceptions.RequestException as e:
        results["error"] = str(e)

    return results

