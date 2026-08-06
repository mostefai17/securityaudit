from urllib.parse import urlparse
from .fetch import fetch
from .headers import security_headers
from .robots import check_robots
from .score import calculate_score
from .sitemap import check_sitemap
from .ssl_check import runsslaudit
from .website import website_check


def run_security_audit(url : str) -> dict:

    # Receiving url
    url = url.strip()
    if not url.startswith(("https://", "http://")):
        url = "https://" + url

    parsed_url = urlparse(url)
    if not parsed_url.netloc or not parsed_url.scheme:
        return {"error": "Invalid URL"}

    host = parsed_url.hostname

    response = fetch(url)

    website_results = website_check(url, response)
    headers_results = security_headers(response)

    if host:
        ssl_results = runsslaudit(host)
    else:
        ssl_results = {"error": "No hostname found in the URL."}

    robots_results = check_robots(url)
    sitemap_results = check_sitemap(url)

    audit_results = {
        "website": website_results,
        "headers": headers_results,
        "ssl": ssl_results,
        "robots": robots_results,
        "sitemap": sitemap_results,
        "score": calculate_score(website_results, headers_results, ssl_results, robots_results, sitemap_results),
    }

    final_url = website_results.get("final_url") or (response.url if response else url)
    status_code = website_results.get("status_code")

    return {
        "url": final_url,
        "audit_results": audit_results,
        "status_code": status_code,
        "url_final_boss": final_url,
    }





