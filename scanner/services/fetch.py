import requests
from django.http import JsonResponse


def fetch(url: str):
    try:
        response = requests.get(
            url,
            timeout=5,
            allow_redirects=True,
            headers={'User-Agent': "SecurityAuditBot/1.0"}
        )
        return response
    except requests.exceptions.RequestException:
        return None

