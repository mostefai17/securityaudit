from django.urls import path

from .views import robots, sitemap_audit

urlpatterns = [
    path('robots.txt', robots, name='robots'),
    path('api/audit-sitemap/', sitemap_audit, name='sitemap_audit')
]
