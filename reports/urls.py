from rest_framework.routers import DefaultRouter

from .views import ReportViewset, YorubaLGAAPIView
from django.urls import path

router = DefaultRouter()

router.register(r"reports", ReportViewset)

urlpatterns = router.urls

urlpatterns += [
    path("yoruba-lgas/", YorubaLGAAPIView.as_view())
]