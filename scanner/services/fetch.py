import requests
from django.template.defaulttags import url


def fetch(url: str):
    try:
        response = requests.get(
            url,
            timeout=5,
            allow_redirects=True,
            headers={'User-Agent': "SecurityAuditBot/1.0"}
        )
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error fetching URL: {e}"

