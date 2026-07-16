from rest_framework import routers
from django.urls import path

from .views import (
    PatrolTeamViewSet,
    PatrolMissionViewSet,
    VehicleViewSet,
    GPSPositionViewSet,
    PatrolEquipmentViewSet,
    PatrolShiftViewSet,
    PatrolDashboardAPIView,
    PatrolMapAPIView,
)

router = routers.DefaultRouter()

router.register("patrol-teams", PatrolTeamViewSet)
router.register("patrol-missions", PatrolMissionViewSet)
router.register("vehicles", VehicleViewSet)
router.register("gps", GPSPositionViewSet)
router.register("equipment", PatrolEquipmentViewSet)
router.register("shifts", PatrolShiftViewSet)
router.register("dashboard", PatrolDashboardAPIView, basename="patrol-dashboard")
router.register("map", PatrolMapAPIView, basename="patrol-map")

urlpatterns = router.urls