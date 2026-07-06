from django.urls import path
from .views import (
    role_redirect,
    citizen_dashboard_view,
    officer_dashboard_view,
    dispatcher_dashboard_view,
    admin_dashboard_view,
    camera_grid_view,
)

urlpatterns = [
    path("", role_redirect, name="dashboard-redirect"),
    path("citizen/", citizen_dashboard_view, name="citizen-dashboard"),
    path("officer/", officer_dashboard_view, name="officer-dashboard"),
    path("dispatcher/", dispatcher_dashboard_view, name="dispatcher-dashboard"),
    path("admin/", admin_dashboard_view, name="admin-dashboard"),
    path("cameras/", camera_grid_view, name="camera-grid"),
]


from django.urls import path

from .views import *

from .widgets.search import *
from .widgets.notifications import *
from .widgets.map import *

from .widgets.admin import *
from .widgets.incidents import *
from .widgets.patrol import *

from .widgets.weather import *
from .widgets.traffic import *

from .widgets.ai import *
from .widgets.security import *
from .widgets.analytics import *

urlpatterns = [

    # Dashboard Pages

    path("admin/", admin_dashboard, name="admin-dashboard"),
    path("super-admin/", super_admin_dashboard, name="super-admin-dashboard"),
    path("police/", police_dashboard, name="police-dashboard"),
    path("amotekun/", amotekun_dashboard, name="amotekun-dashboard"),
    path("dispatcher/", dispatcher_dashboard, name="dispatcher-dashboard"),
    path("analyst/", analyst_dashboard, name="analyst-dashboard"),
    path("facility/", facility_dashboard, name="facility-dashboard"),
    path("citizen/", citizen_dashboard, name="citizen-dashboard"),
    path("responder/", responder_dashboard, name="responder-dashboard"),
    path("ai/", ai_dashboard, name="ai-dashboard"),
    path("auditor/", auditor_dashboard, name="auditor-dashboard"),

    # Global

    path("search/", search_global, name="search-global"),
    path("notifications/", notification_list, name="notification-list"),
    path("map/", dashboard_map, name="dashboard-map"),

    # Admin

    path("widgets/admin/stats/", admin_stats_widget, name="admin-stats-widget"),
    path("widgets/recent-incidents/", recent_incidents_widget, name="recent-incidents-widget"),
    path("widgets/live-activity/", live_activity_widget, name="live-activity-widget"),
    path("widgets/patrol-status/", patrol_status_widget, name="patrol-status-widget"),

    # Shared

    path("widgets/weather/", weather_widget, name="weather-widget"),
    path("widgets/traffic/", traffic_widget, name="traffic-widget"),
    path("widgets/ai-summary/", ai_summary_widget, name="ai-summary-widget"),

    # Super Admin

    path("widgets/security-center/", security_center_widget, name="security-center-widget"),
    path("widgets/ai-cluster/", ai_cluster_widget, name="ai-cluster-widget"),
    path("widgets/api-health/", api_health_widget, name="api-health-widget"),
    path("widgets/system-alert/", system_alert_widget, name="system-alert-widget"),
    path("widgets/state-performance/", state_performance_widget, name="state-performance-widget"),
    path("widgets/lga-performance/", lga_performance_widget, name="lga-performance-widget"),
    path("widgets/national-hotspot/", national_hotspot_widget, name="national-hotspot-widget"),
    path("widgets/feature-flags/", feature_flag_widget, name="feature-flag-widget"),
    path("widgets/global-audit/", global_audit_widget, name="global-audit-widget"),
    path("widgets/platform-activity/", live_platform_activity, name="live-platform-activity"),
    path("widgets/ai-recommendations/", ai_recommendation_widget, name="ai-recommendation-widget"),
]