from .score import calculate_score
from .headers import security_headers
from .ssl_check import runsslaudit
from .sitemap import check_sitemap
from .website import website_check
from .robots import check_robots


def run_security_audit(url : str) -> dict:

    # Recieving url

    url = url.strip()
    if url.startswith(("https://", "http://")):
        pass
    else:
        url = "https://" + url

    website_results = website_check(url)
    robots_results = check_robots(url)
    ssl_results = runsslaudit(url)
    headers_results = security_headers(url)
    sitemap_results = check_sitemap(url)

    audit_results = {
        "website": website_results,
        "headers": headers_results,
        "ssl": ssl_results,
        "robots": robots_results,
        "score": calculate_score(website_results,headers_results,ssl_results,robots_results,sitemap_results),
        "sitemap": sitemap_results
    }

    return {
        "url": url,
        "audit": audit_results,
        "status_code": website_results["status_code"],
        "final_url": website_results["final_url"],
    }





