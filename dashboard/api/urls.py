from django.urls import path

from . import views

urlpatterns = [

    path(
        "incidents/",
        views.IncidentGeoAPIView.as_view(),
        name="api-incidents",
    ),

    path(
        "patrols/",
        views.PatrolGeoAPIView.as_view(),
        name="api-patrols",
    ),

    path(
        "facilities/",
        views.FacilityGeoAPIView.as_view(),
        name="api-facilities",
    ),

    path(
        "weather/",
        views.WeatherAPIView.as_view(),
        name="api-weather",
    ),

    path(
        "dashboard-summary/",
        views.DashboardSummaryAPIView.as_view(),
        name="api-dashboard-summary",
    ),

    path(
    "states/",
    views.StateGeoAPIView.as_view(),
    name="api-states",
),

path(
    "lgas/",
    views.LGAGeoAPIView.as_view(),
    name="api-lgas",
),

path(
    "hotspots/",
    views.HotspotAPIView.as_view(),
    name="api-hotspots",
),

path(
    "cameras/",
    views.CameraAPIView.as_view(),
    name="api-cameras",
),

path(
    "traffic/",
    views.TrafficAPIView.as_view(),
    name="api-traffic",
),

]