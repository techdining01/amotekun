from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseForbidden, HttpResponse

from dashboard.services.dashboard_service import DashboardService
from accounts.choices import UserRole
from accounts.forms import UserCreationForm


# ---------------------------------------------------------------------------
# Role → URL name mapping
# ---------------------------------------------------------------------------
ROLE_DASHBOARD = {
    UserRole.SUPER_ADMIN:         "super-admin-dashboard",
    UserRole.PLATFORM_ADMIN:      "admin-dashboard",
    UserRole.STATE_COMMANDER:     "amotekun-dashboard",
    UserRole.LGA_COMMANDER:       "amotekun-dashboard",
    UserRole.STATION_COMMANDER:   "amotekun-dashboard",
    UserRole.DISPATCHER:          "dispatcher-dashboard",
    UserRole.PATROL_SUPERVISOR:   "police-dashboard",
    UserRole.PATROL_OFFICER:      "officer-dashboard",
    UserRole.RESPONDER:           "responder-dashboard",
    UserRole.ANALYST:             "analyst-dashboard",
    UserRole.AUDITOR:             "auditor-dashboard",
    UserRole.CCTV_OPERATOR:       "officer-dashboard",
    UserRole.EMERGENCY_OPERATOR:  "dispatcher-dashboard",
    UserRole.AGENCY_STAFF:        "facility-dashboard",
    UserRole.CITIZEN:             "citizen-dashboard",
}

# Roles allowed to access each dashboard view
_ADMIN_ROLES = {
    UserRole.SUPER_ADMIN,
    UserRole.PLATFORM_ADMIN,
}
_COMMAND_ROLES = _ADMIN_ROLES | {
    UserRole.STATE_COMMANDER,
    UserRole.LGA_COMMANDER,
    UserRole.STATION_COMMANDER,
}
_OPS_ROLES = _COMMAND_ROLES | {
    UserRole.PATROL_SUPERVISOR,
    UserRole.DISPATCHER,
    UserRole.EMERGENCY_OPERATOR,
    UserRole.ANALYST,
}

DASHBOARD_ALLOWED_ROLES = {
    "super-admin-dashboard":  {UserRole.SUPER_ADMIN},
    "admin-dashboard":        _ADMIN_ROLES,
    "amotekun-dashboard":     _COMMAND_ROLES,
    "police-dashboard":       _COMMAND_ROLES | {UserRole.PATROL_SUPERVISOR},
    "dispatcher-dashboard":   _OPS_ROLES | {UserRole.RESPONDER},
    "responder-dashboard":    _OPS_ROLES | {UserRole.RESPONDER, UserRole.PATROL_OFFICER, UserRole.CCTV_OPERATOR},
    "officer-dashboard":      _OPS_ROLES | {UserRole.PATROL_OFFICER, UserRole.CCTV_OPERATOR, UserRole.RESPONDER},
    "analyst-dashboard":      _OPS_ROLES,
    "ai-dashboard":           _OPS_ROLES,
    "auditor-dashboard":      _ADMIN_ROLES | {UserRole.ANALYST, UserRole.AUDITOR},
    "facility-dashboard":     _OPS_ROLES | {UserRole.AGENCY_STAFF, UserRole.RESPONDER},
    "citizen-dashboard":      set(UserRole),  # all roles can see citizen portal
}


def _require_role(request, view_name):
    """Return HttpResponseForbidden if user's role is not allowed, else None."""
    allowed = DASHBOARD_ALLOWED_ROLES.get(view_name, set())
    if request.user.role not in allowed:
        return HttpResponseForbidden(
            f"<h2>403 — Access Denied</h2>"
            f"<p>Your role ({request.user.role}) cannot access this dashboard.</p>"
            f'<a href="/dashboard/">Go to my dashboard</a>'
        )
    return None


@login_required
def role_redirect(request):
    """Redirect the authenticated user to their role-specific dashboard."""
    url_name = ROLE_DASHBOARD.get(request.user.role, "citizen-dashboard")
    return redirect(reverse(url_name))


@login_required
def add_user(request):
    """View to add a new user via modal."""
    # Only allow admins
    if request.user.role not in _ADMIN_ROLES:
        return HttpResponseForbidden("Not allowed")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={"HX-Trigger": "userAdded"})
    else:
        form = UserCreationForm()
    return render(request, "dashboard/add_user_modal.html", {"form": form})


# ---------------------------------------------------------------------------
# Dashboard views
# ---------------------------------------------------------------------------

@login_required
def citizen_dashboard(request):
    context = DashboardService(request.user).citizen()
    context["role_display"] = "Citizen"
    return render(request, "dashboard/citizen_dashboard.html", context)


@login_required
def officer_dashboard(request):
    denied = _require_role(request, "officer-dashboard")
    if denied: return denied
    svc = DashboardService(request.user)
    context = {
        "role_display": "Security Officer",
        "active_assignments": 0,
        "completed_today": 0,
        "pending_alerts": 0,
        "cameras_online": 0,
        "assignments": [],
        "cameras": [],
        "notifications": svc.notifications.citizen(request.user),
        "ai": svc.ai.dashboard_summary(),
    }
    return render(request, "dashboard/officer_dashboard.html", context)


@login_required
def dispatcher_dashboard(request):
    denied = _require_role(request, "dispatcher-dashboard")
    if denied: return denied
    svc = DashboardService(request.user)
    from dispatch.models import Dispatch
    from reports.models import Incident
    context = {
        "role_display": "Dispatcher",
        "pending_dispatches": Dispatch.objects.filter(status="PENDING").count(),
        "available_units": 0,
        "active_calls": Dispatch.objects.filter(status="ACTIVE").count(),
        "average_eta": "N/A",
        "recent_incidents": Incident.objects.order_by("-created_at")[:10],
        "notifications": svc.notifications.citizen(request.user),
        "ai": svc.ai.dashboard_summary(),
    }
    return render(request, "dashboard/dispatcher_dashboard.html", context)


@login_required
def responder_dashboard(request):
    denied = _require_role(request, "responder-dashboard")
    if denied: return denied
    context = DashboardService(request.user).responder()
    return render(request, "dashboard/responder_dashboard.html", context)


@login_required
def police_dashboard(request):
    denied = _require_role(request, "police-dashboard")
    if denied: return denied
    svc = DashboardService(request.user)
    from dispatch.models import Dispatch
    from reports.models import Incident
    from surveillance.models import Camera
    context = {
        "role_display": "Police",
        "assigned_incidents": Incident.objects.filter(status="OPEN").count(),
        "active_patrols": 0,
        "officers_online": 0,
        "emergency_calls": Dispatch.objects.filter(status="ACTIVE").count(),
        "recent_incidents": Incident.objects.order_by("-created_at")[:10],
        "patrols": [],
        "cameras": Camera.objects.order_by("-created_at")[:6],
        "recommendations": [],
        "notifications": svc.notifications.citizen(request.user),
        "ai": svc.ai.dashboard_summary(),
    }
    return render(request, "dashboard/police_dashboard.html", context)


@login_required
def amotekun_dashboard(request):
    denied = _require_role(request, "amotekun-dashboard")
    if denied: return denied
    svc = DashboardService(request.user)
    context = {
        "role_display": "Amotekun",
        "active_patrols": 0,
        "village_reports": 0,
        "forest_alerts": 0,
        "intelligence_tips": 0,
        "notifications": svc.notifications.citizen(request.user),
        "ai": svc.ai.dashboard_summary(),
    }
    return render(request, "dashboard/amotekun_dashboard.html", context)


@login_required
def analyst_dashboard(request):
    denied = _require_role(request, "analyst-dashboard")
    if denied: return denied
    context = DashboardService(request.user).analyst()
    context["role_display"] = "Security Analyst"
    return render(request, "dashboard/analyst_dashboard.html", context)


@login_required
def admin_dashboard(request):
    denied = _require_role(request, "admin-dashboard")
    if denied: return denied
    context = DashboardService(request.user).admin()
    context["role_display"] = "Administrator"
    return render(request, "dashboard/admin_dashboard.html", context)


@login_required
def super_admin_dashboard(request):
    denied = _require_role(request, "super-admin-dashboard")
    if denied: return denied
    context = DashboardService(request.user).super_admin()
    context["role_display"] = "Super Administrator"
    return render(request, "dashboard/super_admin_dashboard.html", context)


@login_required
def facility_dashboard(request):
    denied = _require_role(request, "facility-dashboard")
    if denied: return denied
    svc = DashboardService(request.user)
    from reports.models import Incident
    context = {
        "role_display": "Facility Manager",
        "total_facilities": 0,
        "ambulances": 0,
        "firestations": 0,
        "available_staff": 0,
        "recent_incidents": Incident.objects.order_by("-created_at")[:10],
        "notifications": svc.notifications.citizen(request.user),
        "ai": svc.ai.dashboard_summary(),
    }
    return render(request, "dashboard/facility_dashboard.html", context)


@login_required
def ai_dashboard(request):
    denied = _require_role(request, "ai-dashboard")
    if denied: return denied
    svc = DashboardService(request.user)
    context = {
        "role_display": "AI Operator",
        "prediction_accuracy": "N/A",
        "threat_score": 0,
        "ai_alerts": 0,
        "models_running": 0,
        "notifications": svc.notifications.citizen(request.user),
        "ai": svc.ai.dashboard_summary(),
    }
    return render(request, "dashboard/ai_dashboard.html", context)


@login_required
def auditor_dashboard(request):
    denied = _require_role(request, "auditor-dashboard")
    if denied: return denied
    context = DashboardService(request.user).auditor()
    context["role_display"] = "Auditor"
    return render(request, "dashboard/auditor_dashboard.html", context)


@login_required
def operations_map(request):
    from decouple import config as env
    context = {
        "role_display": "Operations Map",
        "owm_api_key": env("OPENWEATHER_API_KEY", default=""),
        "GOOGLE_MAP_API_KEY": env("GOOGLE_MAP_API_KEY", default=""),
    }
    return render(request, "dashboard/operations_map.html", context)
