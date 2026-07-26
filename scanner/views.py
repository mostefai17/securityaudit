from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET
import xml.etree.ElementTree as ET
from urllib.parse import urlsplit, urljoin
import requests
from .forms import WebsiteForm
# Create your views here.

def get_website_name(request):
    if request.method == 'POST':
        form = WebsiteForm(request.POST)

        if form.is_valid():
            website = form.cleaned_data['website']
            website_name = urlsplit(website).netloc
            return HttpResponseRedirect('success')

        form = WebsiteForm()
        return render(request, 'name.html', {'form': form})


@require_GET
def robots(request):
    url_param = request.GET.get('url')

    if url_param:
        target_url = url_param.rstrip('/')
        if not target_url.endswith('/robots.txt'):
            target_url = f'{target_url}/robots.txt'

        try:
            response = requests.get(target_url, timeout=5)
            response.raise_for_status()
            return HttpResponse(response.text, content_type='text/plain; charset=utf-8')
        except requests.RequestException as exc:
            return HttpResponse(
                f'Unable to fetch robots.txt: {exc}',
                status=502,
                content_type='text/plain; charset=utf-8',
            )

    return render(request, 'robots.txt', content_type='text/plain; charset=utf-8')


def sitemap_audit(request):
    """Making sure that target url starts with a protocol"""
    url= request.GET.get('url') or request.GET.get('domain')

    if not url or not isinstance(url, str):
        return JsonResponse({'error': 'A valid domain or URL parameter is required.'}, status=400)

        # Clean any accidental whitespace characters
    url = url.strip()

    if not url.startswith(("https://", "http://")):
        url = "https://" + url

    sitemap_url = urljoin(url, '/sitemap.xml')
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

        if response.status_code == 200:
            result["exists"] = True

            try:
                root = ET.fromstring(response.text)
                result["is_valid_xml"] = True

                urls = root.findall('.//loc')
                sitemap = root.findall('.//sitemap')

                result["url_count"] = len(urls) if urls else len(sitemap)

            except ET.ParseError:
                result["is_valid_xml"] = False
                result["error_message"] = "File found but it's not valid XML"
        else:
            result["error_message"] = f"HTTP error {response.status_code}"

    except requests.exceptions.RequestException as e:
        result["error_message"] = f"Network connection failed: {str(e)}"

    return JsonResponse(result)

