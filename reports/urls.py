from rest_framework.routers import DefaultRouter

from .views import IncidentViewset, StateLGAAPIView, YorubaLGAAPIView
from django.urls import path

router = DefaultRouter()

router.register(r"incidents", IncidentViewset, basename="incident")

urlpatterns = router.urls

urlpatterns += [
    path("yoruba-lgas/", YorubaLGAAPIView.as_view()),
    path(
        "state-lgas/<str:state_name>/",
        StateLGAAPIView.as_view(),
    ),
]
