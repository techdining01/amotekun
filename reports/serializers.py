from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Incident, LGA


class IncidentSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Incident

        geo_field = "geometry"

        fields = (
            "id",
            "title",
            "description",
            "report_type",
            "state",
            "lga",
            "created_at",
        )


class LGASerializer(GeoFeatureModelSerializer):
    class Meta:
        model = LGA

        geo_field = "geometry"

        fields = (
            "id",
            "name",
        )
