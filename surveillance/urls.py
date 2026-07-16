from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CameraViewSet, CameraRecordingViewSet, CameraAlertViewSet, camera_grid_view

router = DefaultRouter()
router.register(r'cameras', CameraViewSet, basename='camera')
router.register(r'recordings', CameraRecordingViewSet, basename='recording')
router.register(r'alerts', CameraAlertViewSet, basename='alert')

urlpatterns = [
    path('', include(router.urls)),
    path('grid/', camera_grid_view, name='camera-grid'),
]
