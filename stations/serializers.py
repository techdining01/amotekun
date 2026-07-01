from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import PoliceStation, AmotekunStation, Hospital


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


class HospitalSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Hospital
        geo_field = "location"
        fields = ("id", "name", "address", "state", "lga", "has_emergency")
