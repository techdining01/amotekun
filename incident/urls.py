"""
URL configuration for incident project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.views.generic.base import RedirectView
from django.http import HttpResponse
from .views import home
import reports.urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path(".well-known/appspecific/com.chrome.devtools.json", lambda r: HttpResponse(status=204)),
    path("sw.js", RedirectView.as_view(url="/static/js/sw.js", permanent=False)),
    path("api/accounts/", include("accounts.views.urls")),
    path("api/geography/", include("geography.urls")),
    path("api/", include(reports.urls)),
    path("api/stations/", include("stations.urls")),
    path("api/dispatch/", include("dispatch.urls")),
    path("api/chat/", include("chat.urls")),
    path("chat/", include("chat.urls")),
    path("api/surveillance/", include("surveillance.urls")),
    path("surveillance/", include("surveillance.urls")),
    path("api/traffic/", include("traffic.urls")),
    path("api/analytics/", include("analytics.urls")),
    path("api/mobile/", include("mobile.urls")),
    path("api/patrol/", include("patrol.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("", home, name="home"),
]
