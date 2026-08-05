from django.urls import path

from . import views
urlpatterns = [
    path('', views.get_website_name, name='home'),
    path('robots.txt', views.check_robots, name='check_robots'),
    path('api/audit-sitemap/', views.sitemap_audit, name='sitemap_audit')
]
