from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HotspotViewSet, HotspotAnalysisViewSet, PredictTrafficAPIView

router = DefaultRouter()
router.register(r"hotspots", HotspotViewSet, basename="hotspot")
router.register(r"analyses", HotspotAnalysisViewSet, basename="hotspot-analysis")

urlpatterns = [
    path("", include(router.urls)),
    path("predict/", PredictTrafficAPIView.as_view(), name="predict-traffic"),
]
