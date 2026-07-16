from rest_framework import serializers

from reports.models import Incident
from patrol.models import PatrolTeam
from stations.serializers import FacilitySerializer
from traffic.models import Weather


facility_serializer = FacilitySerializer()

class IncidentSerializer(serializers.ModelSerializer):

    class Meta:

        model = Incident

        fields = (
            "id",
            "title",
            "incident_type",
            "status",
            "latitude",
            "longitude",
            "reported_at",
        )


class PatrolTeamSerializer(serializers.ModelSerializer):

    class Meta:

        model = PatrolTeam

        fields = (
            "id",
            "code",
            "status",
            "latitude",
            "longitude",
            "team",
            "vehicle",
        )
  

class WeatherSerializer(serializers.ModelSerializer):

    class Meta:

        model = Weather

        fields = (
            "temperature",
            "humidity",
            "wind_speed",
            "rainfall",
        )