from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MobileDeviceViewSet, PushNotificationViewSet, MobileTokenObtainPairView
from .views import MobileIncidentViewSet, FacilityViewSet, MobileDispatchViewSet, MediaUploadViewSet, MediaListView

router = DefaultRouter()
router.register(r'devices', MobileDeviceViewSet, basename='mobiledevice')
router.register(r'notifications', PushNotificationViewSet, basename='pushnotification')
router.register(r'incidents', MobileIncidentViewSet, basename='mobile-incident')
router.register(r'facilities', FacilityViewSet, basename='facility')
router.register(r'dispatch', MobileDispatchViewSet, basename='mobile-dispatch')
router.register(r'media', MediaUploadViewSet, basename='media-upload')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', MobileTokenObtainPairView.as_view(), name='mobile_token_obtain_pair'),
    path('incidents/<int:incident_id>/media/', MediaListView.as_view(), name='incident-media'),
]
