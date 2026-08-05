from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_GET
from urllib.parse import urlsplit
from .forms import WebsiteForm
from .services.sitemap import check_sitemap
from django.shortcuts import render
from .services.audit import run_security_audit
# Create your views here.

def get_website_name(request):
    if request.method == 'POST':
        form = WebsiteForm(request.POST)

        if form.is_valid():
            website = form.cleaned_data['website']
            website_name = urlsplit(website).netloc
            return redirect(reverse("scanner:home") + f"?url={website_name}")
        return render(request, "scanner/form.html", {'form': form})
    else:
        form = WebsiteForm()
        return render(request, 'scanner/form.html', {'form': form})


@require_GET
def check_robots(request):
    url_param = request.GET.get('url')
    if not url_param:
        return JsonResponse({'error': 'URL parameter is required.'}, status=400)

    result = check_robots(url_param)
    return JsonResponse(result)


def sitemap_audit(request):
    url_param = request.GET.get('url') or request.GET.get('domain')
    if not url_param or not isinstance(url_param, str):
        return JsonResponse({'error': 'Invalid URL or domain provided.'}, status=400)

    result = check_sitemap(url_param)
    return JsonResponse(result)

def audit_view(request):
    result = None
    error = None

    if request.method == 'POST':
        form = WebsiteForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['website']
            result = {'url', url}
            if 'error' in result:
                error = result['error']
    else:
        form = WebsiteForm()

    return render(request, 'scanner/audit.html', {
        'form': form,
        'result': result,
        'error': error,
    })

