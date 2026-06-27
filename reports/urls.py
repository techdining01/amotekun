from rest_framework.routers import DefaultRouter

from .views import IncidentViewset, StateLGAAPIView, YorubaLGAAPIView, HotspotAPIView, LGACentroidAPIView, IncidentTypeFilterView, incident_create_view, IncidentCreateAPIView
from django.urls import path

router = DefaultRouter()

router.register(r"incidents", IncidentViewset, basename="incident")

urlpatterns = router.urls

urlpatterns += [
    path("yoruba-lgas/", YorubaLGAAPIView.as_view()),

    path(
        "state-lgas/<str:state_name>/",
        StateLGAAPIView.as_view(),
        name="state-lgas",
    ),
    
    path(
        "hotspots/",
        HotspotAPIView.as_view(),
        name="hotspots",
    ),
    
    path(
        "lga-centroid/<int:pk>/",
        LGACentroidAPIView.as_view(),
        name="lga-centroid",
    ),
    
    path(
        "incidents/type/<str:report_type>/",
        IncidentTypeFilterView.as_view(),
        name="incidents-by-type",
    ),
     
    path(
        "incident-create/",
        incident_create_view,
        name="incident-create",
    ),
    
    path(
        "api/incident-create/",
        IncidentCreateAPIView.as_view(),
        name="api-incident-create",
    ),
]
