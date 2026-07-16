from django.urls import path, include
from dashboard.views import (
    role_redirect,
    admin_dashboard,
    super_admin_dashboard,
    police_dashboard,
    amotekun_dashboard,
    dispatcher_dashboard,
    analyst_dashboard,
    facility_dashboard,
    citizen_dashboard,
    responder_dashboard,
    officer_dashboard,
    ai_dashboard,
    auditor_dashboard,
    operations_map,
    add_user,
)

from dashboard.widgets.search import search_global
from dashboard.widgets.notifications import notification_list, mark_all_read, clear_all_notifications
from dashboard.widgets.map import dashboard_map

from dashboard.widgets.admin import admin_stats_widget, live_activity_widget
from dashboard.widgets.incidents import recent_incidents_widget
from dashboard.widgets.patrol import patrol_status_widget

from dashboard.widgets.weather import weather_widget
from dashboard.widgets.traffic import traffic_widget

from dashboard.widgets.ai import (
    ai_summary_widget,
    ai_cluster_widget,
    ai_recommendation_widget,
)
from dashboard.widgets.security import (
    security_center_widget,
    api_health_widget,
    system_alert_widget,
    global_audit_widget,
    feature_flag_widget,
)
from dashboard.widgets.analyst import (
    state_performance_widget,
    lga_performance_widget,
    national_hotspot_widget,
    live_platform_activity,
)
from dashboard.widget_views import map_widget, activity_widget
from dashboard.map_api import map_incidents, map_facilities, map_traffic, map_weather


urlpatterns = [
    # Role-based redirect — LOGIN_REDIRECT_URL should point here
    path("", role_redirect, name="dashboard-redirect"),

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
    path("officer/", officer_dashboard, name="officer-dashboard"),
    path("ai/", ai_dashboard, name="ai-dashboard"),
    path("auditor/", auditor_dashboard, name="auditor-dashboard"),
    path("operations-map/", operations_map, name="operations-map"),

    # Global
    path("add-user/", add_user, name="add-user"),
    path("search/", search_global, name="search-global"),
    path("notifications/", notification_list, name="notification-list"),
    path("notifications/mark-read/", mark_all_read, name="notification-mark-read"),
    path("notifications/clear/", clear_all_notifications, name="notification-clear"),
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
    path("widgets/map/", map_widget, name="map-widget"),
    path("widgets/activity/", activity_widget, name="activity-widget"),

    # Map data API
    path("api/map/incidents/", map_incidents, name="map-incidents"),
    path("api/map/facilities/", map_facilities, name="map-facilities"),
    path("api/map/traffic/", map_traffic, name="map-traffic"),
    path("api/map/weather/", map_weather, name="map-weather"),

    # API
    path("api/dashboard/", include("dashboard.api.urls")),
]

# from dashboard.views.widget_views import *

# urlpatterns += [

#     path(

#         "widgets/statistics/",

#         statistics_widget,

#         name="statistics-widget",

#     ),

#     path(

#         "widgets/activity/",

#         activity_widget,

#         name="activity-widget",

#     ),

#     path(

#         "widgets/notifications/",

#         notification_widget,

#         name="notification-widget",

#     ),

#     path(

#         "widgets/map/",

#         map_widget,

#         name="map-widget",

#     ),

#     path(

#         "widgets/ai/",

#         ai_summary_widget,

#         name="ai-summary-widget",

#     ),

#     path(

#         "widgets/responder/",

#         responder_widget,

#         name="responder-widget",

#     ),

# ]