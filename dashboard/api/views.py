from rest_framework.response import Response
from rest_framework.views import APIView

from reports.models import Incident, State, LGA
from patrol.models import PatrolTeam
from stations.models import Facility
from stations.serializers import FacilitySerializer
from traffic.models import Weather



from surveillance.models import Camera

from analytics.services.prediction_service import PredictionService

from surveillance.models import CameraAlert


from .serializers import (
    IncidentSerializer,
    PatrolTeamSerializer,
    WeatherSerializer,
)


class DashboardSummaryAPIView(APIView):

    def get(self, request):

        data = {

            "incidents": Incident.objects.count(),

            "active_incidents": Incident.objects.filter(
                status="ACTIVE"
            ).count(),

            "resolved_incidents": Incident.objects.filter(
                status="RESOLVED"
            ).count(),

            "patrols": PatrolTeam.objects.count(),

            "active_patrols": PatrolTeam.objects.filter(
                status="ACTIVE"
            ).count(),

            "facilities": Facility.objects.count(),

            "weather_records": Weather.objects.count(),

        }

        return Response(data)


class IncidentGeoAPIView(APIView):

    def get(self, request):

        qs = Incident.objects.all()

        serializer = IncidentSerializer(
            qs,
            many=True,
        )

        return Response(serializer.data)


class PatrolGeoAPIView(APIView):

    def get(self, request):

        qs = PatrolTeam.objects.select_related(
            "team",
            "vehicle",
        )

        serializer = PatrolTeamSerializer(
            qs,
            many=True,
        )

        return Response(serializer.data)


class FacilityGeoAPIView(APIView):

    def get(self, request):

        serializer = FacilitySerializer(

            Facility.objects.all(),

            many=True,

        )

        return Response(serializer.data)


class WeatherAPIView(APIView):

    def get(self, request):

        latest = Weather.objects.order_by(
            "-recorded_at"
        ).first()

        if latest:

            return Response(
                WeatherSerializer(latest).data
            )

        return Response({})

class StateGeoAPIView(APIView):

    def get(self, request):

        features = []

        for state in State.objects.all():

            features.append({

                "type": "Feature",

                "geometry": state.geometry,

                "properties": {

                    "id": state.id,

                    "name": state.name,

                },

            })

        return Response({

            "type": "FeatureCollection",

            "features": features,

        })


class LGAGeoAPIView(APIView):

    def get(self, request):

        features = []

        for lga in LGA.objects.select_related("state"):

            features.append({

                "type": "Feature",

                "geometry": lga.geometry,

                "properties": {

                    "id": lga.id,

                    "name": lga.name,

                    "state": lga.state.name,

                },

            })

        return Response({

            "type":"FeatureCollection",

            "features":features,

        })

class CameraAPIView(APIView):

    def get(self, request):

        cameras = Camera.objects.filter(

            is_active=True

        )

        data = [

            {

                "id":camera.id,

                "name":camera.name,

                "lat":camera.latitude,

                "lng":camera.longitude,

                "status":camera.status,

            }

            for camera in cameras

        ]

        return Response(data)


class HotspotAPIView(APIView):

    def get(self, request):

        prediction_service = PredictionService()
        hotspots = prediction_service.get_all_hotspots()

        return Response(

            [
                {
                    "latitude":h.latitude,

                    "longitude":h.longitude,

                    "risk":h.risk_score,

                }

                for h in hotspots

            ]

        )


class TrafficAPIView(APIView):

    def get(self, request):

        latest=CameraAlert.objects.order_by(

            "-created_at"

        )[:100]

        return Response(

            [

                {

                    "latitude":t.latitude,

                    "longitude":t.longitude,

                    "speed":t.average_speed,

                    "severity":t.congestion_level,

                }

                for t in latest

            ]

        )