from django.urls import path

from .views import check_robots, sitemap_audit

import views
urlpatterns = [
    path('', views.get_website_name, name='home'),
    path('robots.txt', check_robots, name='robots'),
    path('api/audit-sitemap/', sitemap_audit, name='sitemap_audit')
]
