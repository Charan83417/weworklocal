"""
URL configuration for weworklocal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views as core_views
from core.admin_dashboard import admin_dashboard_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/dashboard/', admin_dashboard_view, name='admin_dashboard'),

    # Health check for Docker and load balancers
    path('health/', core_views.health_check, name='health_check'),

    # Core app URLs
    path('', core_views.landing_page, name='landing'),
    path('splash/', core_views.splash_screen, name='splash'),
    path('dashboard/', core_views.dashboard, name='dashboard'),
    path('core/', include('core.urls')),

    # PWA
    path('manifest.json', core_views.pwa_manifest, name='pwa_manifest'),

    # App URLs
    path('auth/', include('authentication.urls')),
    path('subscriptions/', include('subscriptions.urls')),
    path('properties/', include('properties.urls')),
    path('wallets/', include('wallets.urls')),
    path('referrals/', include('referrals.urls')),
    path('support/', include('support.urls')),

    # Django Allauth URLs
    path('accounts/', include('allauth.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
