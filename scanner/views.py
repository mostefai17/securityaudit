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
def check_robots(request):
    url_param = request.GET.get('url')

    result = check_robots(url_param)

    return JsonResponse(result)


def sitemap_audit(request):
    """Making sure that target url starts with a protocol"""
    url= request.GET.get('url') or request.GET.get('domain')

    if not url or not isinstance(url, str):
        return JsonResponse({'error': 'A valid domain or URL parameter is required.'}, status=400)

