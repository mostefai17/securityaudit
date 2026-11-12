import csv
from datetime import timedelta
from urllib.parse import urlsplit

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import DatabaseError
from django.db.models import Avg
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_GET, require_POST

from .forms import CustomUserCreationForm, WebsiteForm
from .models import AuditReport
from .services.audit import run_security_audit
from .services.robots import check_robots as fetch_robots
from .services.sitemap import check_sitemap

# Create your views here.


def get_website_name(request):
    if request.method == "POST":
        form = WebsiteForm(request.POST)

        if form.is_valid():
            website = form.cleaned_data["website"]
            website_name = urlsplit(website).netloc
            return redirect(reverse("scanner:home") + f"?url={website_name}")
        return render(request, "scanner/form.html", {"form": form})
    else:
        form = WebsiteForm()
        return render(request, "scanner/form.html", {"form": form})


@require_GET
def check_robots(request):
    url_param = request.GET.get("url")
    if not url_param:
        return JsonResponse({"error": "URL parameter is required."}, status=400)

    result = fetch_robots(url_param)
    return JsonResponse(result)


def sitemap_audit(request):
    url_param = request.GET.get("url") or request.GET.get("domain")
    if not url_param or not isinstance(url_param, str):
        return JsonResponse({"error": "Invalid URL or domain provided."}, status=400)

    result = check_sitemap(url_param)
    return JsonResponse(result)


def audit_view(request):
    result = None
    error = None

    if request.method == "POST":
        form = WebsiteForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data["website"]
            try:
                result = run_security_audit(url)
                if "error" in result:
                    error = result["error"]
            except Exception as e:  # noqa: BLE001
                error = f"An error occurred during the audit: {e!s}"

            # Persist successful audit to AuditReport for authenticated users
            if not error and result and request.user.is_authenticated:
                try:
                    # Robust extraction: navigate the result dict structure
                    score_value = None
                    if isinstance(result, dict):
                        audit_results = result.get("audit_results") or {}
                        score_obj = audit_results.get("score")
                        if isinstance(score_obj, dict):
                            # score_obj is a dict with 'score' and/or 'security_percentage' keys
                            score_value = score_obj.get("score") or score_obj.get(
                                "security_percentage"
                            )
                        else:
                            # score_obj is a plain number
                            score_value = score_obj

                    # Convert to float
                    if score_value is not None:
                        try:
                            score_float = float(score_value)
                        except (TypeError, ValueError):
                            score_float = None

                        # Debounce: don't save if same user+url within 1 minute
                        if score_float is not None:
                            last_audit = (
                                AuditReport.objects.filter(user=request.user, url=url)
                                .order_by("-created_at")
                                .first()
                            )

                            if not last_audit or (
                                timezone.now() - last_audit.created_at
                            ) > timedelta(minutes=1):
                                AuditReport.objects.create(
                                    user=request.user, url=url, score=score_float
                                )

                # Using DatabaseError to catch any database-related issues, including IntegrityError
                except DatabaseError:
                    # Silently fail on persistence; don't crash the audit view
                    pass
        else:
            form = WebsiteForm()
    else:
        form = WebsiteForm()

    return render(
        request,
        "scanner/audit.html",
        {
            "form": form,
            "result": result,
            "error": error,
        },
    )


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = (request.POST.get("first_name") or "").capitalize()
            user.last_name = (request.POST.get("last_name") or "").capitalize()
            user.save()
            return redirect("scanner:dashboard")
    else:
        form = CustomUserCreationForm()
    return render(request, "scanner/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("scanner:home")
        else:
            return render(
                request,
                "scanner/login.html",
                {"error": "Invalid username or password."},
            )
    return render(request, "scanner/login.html")


@require_POST
def logout_view(request):
    logout(request)
    return redirect("scanner:home")


@login_required(login_url="scanner:login")
def dashboard_view(request):
    reports = AuditReport.objects.filter(user=request.user).order_by("-created_at")

    # Read optional filter GET params
    date_from = request.GET.get("date_from")  # format: YYYY-MM-DD
    date_to = request.GET.get("date_to")
    domain = request.GET.get("domain")

    # Apply filters to the queryset
    if date_from:
        reports = reports.filter(created_at__date__gte=date_from)
    if date_to:
        reports = reports.filter(created_at__date__lte=date_to)
    if domain:
        reports = reports.filter(url__icontains=domain)

    total_audits = reports.count()
    avg_score = reports.aggregate(avg=Avg("score"))["avg"]
    avg_score = round(avg_score, 1) if avg_score is not None else None
    sites_scanned = reports.values("url").distinct().count()
    issues_found = reports.filter(score__lt=50).count()
    recent_audits = reports[:10]

    return render(
        request,
        "scanner/dashboard.html",
        {
            "total_audits": total_audits,
            "avg_score": avg_score,
            "sites_scanned": sites_scanned,
            "issues_found": issues_found,
            "recent_audits": recent_audits,
            "filter_date_from": date_from,
            "filter_date_to": date_to,
            "filter_domain": domain,
        },
    )


@login_required()
def export_reports_csv(request):
    reports = AuditReport.objects.filter(user=request.user).order_by("-created_at")

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="audit_reports.csv"'

    writer = csv.writer(response)
    writer.writerow(["URL", "Score", "Date"])

    for audit in reports:
        writer.writerow([audit.url, audit.score, audit.created_at.strftime("%Y-%m-%d")])

    return response
