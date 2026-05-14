from rest_framework.routers import DefaultRouter

from .views import ReportViewset

router = DefaultRouter()

router.register(r"reports", ReportViewset)

urlpatterns = router.urls



