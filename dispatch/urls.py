from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DispatchViewSet

app_name = "dispatch"

router = DefaultRouter()
router.register("dispatches", DispatchViewSet, basename="dispatch")

urlpatterns = [
    path("", include(router.urls)),
]
