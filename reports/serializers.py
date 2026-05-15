from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Reports, LGA



class ReportsSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = Reports

        geo_field = "geometry"

        fields = (
            "id",
            "title",
            "description",
            "report_type",
            "geometry",
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

