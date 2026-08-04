from urllib.parse import urlsplit, urlunsplit

import requests

def check_robots(url: str) -> dict:

    # validate url
    if not isinstance(url, str) or not url.strip():
        return {"error": "Invalid Url Provider"}

    if not url.startswith(("https://", "http://")):
        url = "https://" + url

    robots_url = url.rstrip("/") + "/robots.txt"

    # Checking if there is missing part
    parts = urlsplit(url)
    if not parts.scheme or parts.netloc:
        return {"error": "Invalid URL Provider"}

    base_url = urlunsplit((parts.scheme, parts.netloc, "", "",""))
    robots_url = base_url.rstrip("/") +"/sitemap.xml"


    result = {
        "url_checked": robots_url,
        "exists": False,
        "status_code": None,
        "is_valid_robots": False,
        "error_message": None,
    }

    try:
        response = requests.get(robots_url, timeout=5)
        if response.ok:
            result["exists"] = True
            result["status_code"] = response.status_code
            result["is_valid_robots"] = True
        else:
            result["error_message"] = f"HTTP error {response.status_code}"

    except requests.RequestException as e:
        return {"error": f"failed to reach target: {str(e)}"}

    return result

