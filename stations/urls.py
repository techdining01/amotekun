from django.urls import path
from .views import NearestStationAPIView, RouteByPgRoutingAPIView

urlpatterns = [
    path("nearest/", NearestStationAPIView.as_view(), name="nearest-station"),
    path("route/", RouteByPgRoutingAPIView.as_view(), name="route-pgrouting"),
]
