from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TrafficIncidentViewSet,
    TrafficFlowViewSet,
    RoadViewSet,
    TrafficCameraViewSet,
    TrafficAlertViewSet,
)

router = DefaultRouter()
router.register(r"incidents", TrafficIncidentViewSet, basename="trafficincident")
router.register(r"flows", TrafficFlowViewSet, basename="trafficflow")
router.register(r"roads", RoadViewSet, basename="road")
router.register(r"cameras", TrafficCameraViewSet, basename="trafficcamera")
router.register(r"snapshots", TrafficSnapshotViewSet, basename="trafficsnapshot")
router.register(r"alerts", TrafficAlertViewSet, basename="trafficalert")

urlpatterns = [
    path("", include(router.urls)),
]
