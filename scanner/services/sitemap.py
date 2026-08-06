
import xml.etree.ElementTree as ET
from urllib.parse import urlsplit, urlunsplit
import requests


def check_sitemap(url: str) -> dict:

    if not isinstance(url, str) or not url.strip():
        return {"error": "Invalid URL provided."}

    if not url.startswith(("https://", "http://")):
        url = "https://" + url

    parts = urlsplit(url)
    if not parts.scheme or not parts.netloc:
        return {"error": "Invalid URLProvider"}
    base_url = urlunsplit((parts.scheme, parts.netloc, "", "",""))
    sitemap_url = base_url.rstrip("/") + "/sitemap.xml"

    result = {
        "url_checked": sitemap_url,
        "exists": False,
        "status_code": None,
        "is_valid_xml": False,
        "url_count": 0,
        "error_message": None
    }

    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) SecurityAuditBot/1.0'}
        response = requests.get(sitemap_url, headers=headers, timeout=10, allow_redirects=True)
        result["status_code"] = response.status_code

        if response.ok:
            result["exists"] = True

            try:
                root = ET.fromstring(response.text)
                result["is_valid_xml"] = True

                urls = root.findall('.//loc')
                sitemaps = root.findall('.//sitemap')

                result["url_count"] = len(urls) if urls else len(sitemaps)

            except ET.ParseError:
                result["is_valid_xml"] = False
                result["error_message"] = "File found but it's not valid XML"
        else:
            result["error_message"] = f"HTTP error {response.status_code}"

    except requests.exceptions.RequestException as e:
        result["error_message"] = f"Network connection failed: {str(e)}"

    return result