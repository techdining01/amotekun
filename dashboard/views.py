from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utils import (
    citizen_required,
    officer_required,
    dispatcher_required,
    admin_required,
    officer_or_higher,
    dispatcher_or_higher,
)


@login_required
def role_redirect(request):
    """
    Redirect user to their role-specific dashboard
    """
    user = request.user
    role = user.role

    role_urls = {
        "CITIZEN": "citizen-dashboard",
        "OFFICER": "officer-dashboard",
        "DISPATCHER": "dispatcher-dashboard",
        "ADMIN": "admin-dashboard",
    }

    dashboard_url = role_urls.get(role, "citizen-dashboard")
    return redirect(dashboard_url)


@login_required
@citizen_required
def citizen_dashboard_view(request):
    """
    Citizen dashboard view
    """
    context = {
        "user": request.user,
        "role": request.user.role,
        "role_display": request.user.get_role_display(),
    }
    return render(request, "dashboard/citizen_dashboard.html", context)


@login_required
@officer_required
def officer_dashboard_view(request):
    """
    Officer dashboard view
    """
    context = {
        "user": request.user,
        "role": request.user.role,
        "role_display": request.user.get_role_display(),
    }
    return render(request, "dashboard/officer_dashboard.html", context)


@login_required
@dispatcher_required
def dispatcher_dashboard_view(request):
    """
    Dispatcher dashboard view
    """
    context = {
        "user": request.user,
        "role": request.user.role,
        "role_display": request.user.get_role_display(),
    }
    return render(request, "dashboard/dispatcher_dashboard.html", context)


@login_required
@admin_required
def admin_dashboard_view(request):
    """
    Admin dashboard view
    """
    context = {
        "user": request.user,
        "role": request.user.role,
        "role_display": request.user.get_role_display(),
    }
    return render(request, "dashboard/admin_dashboard.html", context)


@login_required
@officer_or_higher
def camera_grid_view(request):
    """
    Render a dedicated camera grid page for full 24-camera layout.
    """
    context = {
        "user": request.user,
        "role": request.user.role,
        "role_display": request.user.get_role_display(),
        "grid_page": True,
    }
    return render(request, "dashboard/camera_grid.html", context)



# New views functions for widets

# dashboard/views.py

from django.shortcuts import render


def search_global(request):
    return render(request, "dashboard/widgets/search_results.html")


def notification_list(request):
    return render(request, "dashboard/widgets/notification_list.html")


def dashboard_map(request):
    return render(request, "dashboard/widgets/dashboard_map.html")


def admin_stats_widget(request):
    return render(request, "dashboard/widgets/admin_stats.html")


def recent_incidents_widget(request):
    return render(request, "dashboard/widgets/recent_incidents.html")


def live_activity_widget(request):
    return render(request, "dashboard/widgets/live_activity.html")


def patrol_status_widget(request):
    return render(request, "dashboard/widgets/patrol_status.html")


def security_center_widget(request):
    return render(request, "dashboard/widgets/security_center.html")


def ai_cluster_widget(request):
    return render(request, "dashboard/widgets/ai_cluster.html")


def api_health_widget(request):
    return render(request, "dashboard/widgets/api_health.html")


def system_alert_widget(request):
    return render(request, "dashboard/widgets/system_alert.html")


def state_performance_widget(request):
    return render(request, "dashboard/widgets/state_performance.html")


def lga_performance_widget(request):
    return render(request, "dashboard/widgets/lga_performance.html")


def national_hotspot_widget(request):
    return render(request, "dashboard/widgets/national_hotspot.html")


def feature_flag_widget(request):
    return render(request, "dashboard/widgets/feature_flags.html")


def global_audit_widget(request):
    return render(request, "dashboard/widgets/global_audit.html")


def live_platform_activity(request):
    return render(request, "dashboard/widgets/platform_activity.html")


def ai_recommendation_widget(request):
    return render(request, "dashboard/widgets/ai_recommendations.html")


# new widgets
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def admin_dashboard(request):
    return render(request, "dashboard/admin_dashboard.html")


@login_required
def super_admin_dashboard(request):
    return render(request, "dashboard/super_admin_dashboard.html")


@login_required
def police_dashboard(request):
    return render(request, "dashboard/police_dashboard.html")


@login_required
def amotekun_dashboard(request):
    return render(request, "dashboard/amotekun_dashboard.html")


@login_required
def dispatcher_dashboard(request):
    return render(request, "dashboard/dispatcher_dashboard.html")


@login_required
def analyst_dashboard(request):
    return render(request, "dashboard/analyst_dashboard.html")


@login_required
def facility_dashboard(request):
    return render(request, "dashboard/facility_dashboard.html")


@login_required
def citizen_dashboard(request):
    return render(request, "dashboard/citizen_dashboard.html")


@login_required
def responder_dashboard(request):
    return render(request, "dashboard/responder_dashboard.html")


@login_required
def ai_dashboard(request):
    return render(request, "dashboard/ai_dashboard.html")


@login_required
def auditor_dashboard(request):
    return render(request, "dashboard/auditor_dashboard.html")