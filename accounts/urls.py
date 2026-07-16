from django.urls import path
from . import views

urlpatterns = [

    path(
        "admin/",
        views.AdminDashboardView.as_view(),
        name="admin-dashboard",
    ),

    path(
        "super-admin/",
        views.SuperAdminDashboardView.as_view(),
        name="super-admin-dashboard",
    ),

    path(
        "police/",
        views.PoliceDashboardView.as_view(),
        name="police-dashboard",
    ),

    path(
        "amotekun/",
        views.AmotekunDashboardView.as_view(),
        name="amotekun-dashboard",
    ),

    path(
        "dispatcher/",
        views.DispatcherDashboardView.as_view(),
        name="dispatcher-dashboard",
    ),

    path(
        "analyst/",
        views.AnalystDashboardView.as_view(),
        name="analyst-dashboard",
    ),

    path(
        "facility/",
        views.FacilityDashboardView.as_view(),
        name="facility-dashboard",
    ),

    path(
        "citizen/",
        views.CitizenDashboardView.as_view(),
        name="citizen-dashboard",
    ),

    path(
        "responder/",
        views.ResponderDashboardView.as_view(),
        name="responder-dashboard",
    ),

    path(
        "ai/",
        views.AIDashboardView.as_view(),
        name="ai-dashboard",
    ),

    path(
        "auditor/",
        views.AuditorDashboardView.as_view(),
        name="auditor-dashboard",
    ),

]
