from django.urls import path
from .views import dashboard_view, role_redirect
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", login_required(role_redirect), name="dashboard-redirect"),
    path("citizen/", login_required(dashboard_view), name="citizen-dashboard"),
    path("officer/", login_required(dashboard_view), name="officer-dashboard"),
    path("dispatcher/", login_required(dashboard_view), name="dispatcher-dashboard"),
    path("admin/", login_required(dashboard_view), name="admin-dashboard"),
]
