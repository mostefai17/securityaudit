from django.urls import path

from .views import check_robots, sitemap_audit

urlpatterns = [
    path('robots.txt', check_robots, name='robots'),
    path('api/audit-sitemap/', sitemap_audit, name='sitemap_audit')
]
