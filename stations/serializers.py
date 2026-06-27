from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import PoliceStation, AmotekunStation


class PoliceStationSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = PoliceStation
        geo_field = "location"
        fields = ("id", "name", "address", "state", "lga")


class AmotekunStationSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = AmotekunStation
        geo_field = "location"
        fields = ("id", "name", "address", "state", "lga")
