from django.contrib.auth import authenticate, login, logout
from .forms  import CustomUserCreationForm
from django.db.models import Avg
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST
from urllib.parse import urlsplit
from .forms import WebsiteForm
from .models import AuditReport
from .services.robots import check_robots as fetch_robots
from .services.audit import run_security_audit
from .services.sitemap import check_sitemap
from django.contrib.auth.decorators import login_required

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

    result = fetch_robots(url_param)
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
            try:
                result = run_security_audit(url)
                if 'error' in result:
                    error = result['error']
            except Exception as e:
                error = f"An error occurred during the audit: {str(e)}"
    else:
        form = WebsiteForm()

    return render(request, 'scanner/audit.html', {
        'form': form,
        'result': result,
        'error': error,
    })

def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = (request.POST.get("first_name") or "").capitalize()
            user.last_name = (request.POST.get("last_name") or "").capitalize()
            user.save()
            return redirect("scanner:home")
    else:
        form = CustomUserCreationForm()
    return render(request, 'scanner/register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("scanner:home")
        else:
            return render(request, "scanner/login.html", {"error": "Invalid username or password."})
    return render(request, "scanner/login.html")

@require_POST
def logout_view(request):
    logout(request)
    return redirect("scanner:home")

@login_required(login_url='scanner:login')
def dashboard_view(request):
    reports = AuditReport.objects.filter(user=request.user).order_by('-created_at')
    total_audits = reports.count()
    avg_score = reports.aggregate(avg=Avg('score'))['avg']
    avg_score = round(avg_score, 1) if avg_score is not None else None
    sites_scanned = reports.values('url').distinct().count()
    issues_found = reports.filter(score__lt=50).count()
    recent_audits = reports[:10]
    return render(request, 'scanner/dashboard.html', {
        'total_audits': total_audits,
        'avg_score': avg_score,
        'sites_scanned': sites_scanned,
        'issues_found': issues_found,
        'recent_audits': recent_audits,
    })

