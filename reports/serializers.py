from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers
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
    state_name = serializers.CharField(source='state.name', read_only=True)
    state_id = serializers.IntegerField(source='state.id', read_only=True)

    class Meta:
        model = LGA

        geo_field = "geometry"

        fields = (
            "id",
            "name",
            "state_id",
            "state_name",
        )
