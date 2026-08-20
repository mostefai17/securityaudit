from django.urls import path

from . import views

app_name = "scanner"
urlpatterns = [
    path('', views.audit_view, name='home'),
    path('robots.txt', views.check_robots, name='check_robots'),
    path('api/audit-sitemap/', views.sitemap_audit, name='sitemap_audit'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]
