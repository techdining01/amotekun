from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CameraViewSet, CameraRecordingViewSet, CameraAlertViewSet

router = DefaultRouter()
router.register(r'cameras', CameraViewSet, basename='camera')
router.register(r'recordings', CameraRecordingViewSet, basename='recording')
router.register(r'alerts', CameraAlertViewSet, basename='alert')

urlpatterns = [
    path('', include(router.urls)),
]
