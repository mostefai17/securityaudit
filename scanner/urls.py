from django.urls import path

from . import views

app_name = "scanner"
urlpatterns = [
    path('', views.audit_view, name='home'),
    path('robots.txt', views.check_robots, name='check_robots'),
    path('api/audit-sitemap/', views.sitemap_audit, name='sitemap_audit'),
]
