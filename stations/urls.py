from django.urls import path
from .views import NearestStationAPIView, RouteByPgRoutingAPIView, PoliceStationListAPIView, AmotekunStationListAPIView, HospitalListAPIView

urlpatterns = [
    path("nearest/", NearestStationAPIView.as_view(), name="nearest-station"),
    path("route/", RouteByPgRoutingAPIView.as_view(), name="route-pgrouting"),
    path("police/", PoliceStationListAPIView.as_view(), name="police-station-list"),
    path("amotekun/", AmotekunStationListAPIView.as_view(), name="amotekun-station-list"),
    path("hospitals/", HospitalListAPIView.as_view(), name="hospital-list"),
]
