from django.contrib.gis.geos import Point
from django.db import connection
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import PoliceStation, AmotekunStation, Hospital
from .serializers import PoliceStationSerializer, AmotekunStationSerializer, HospitalSerializer


def _fast_knn_station(table, lon, lat, limit=1):
    sql = (
        "SELECT id, name, address, state, lga, ST_AsGeoJSON(location) AS geom "
        f"FROM {table} "
        "ORDER BY location <-> ST_SetSRID(ST_MakePoint(%s, %s), 4326) "
        "LIMIT %s"
    )
    with connection.cursor() as cur:
        cur.execute(sql, [lon, lat, limit])
        cols = [c[0] for c in cur.description]
        rows = [dict(zip(cols, r)) for r in cur.fetchall()]
    return rows


class NearestStationAPIView(APIView):
    """GET /api/stations/nearest/?lat=..&lon=..&type=police|amotekun&limit=1"""

    def get(self, request):
        try:
            lat = float(request.query_params.get("lat"))
            lon = float(request.query_params.get("lon"))
        except Exception:
            return Response({"detail": "Provide numeric lat and lon"}, status=400)

        stype = request.query_params.get("type", "police").lower()
        limit = int(request.query_params.get("limit", 1))

        if stype == "police":
            table = "stations_policestation"
        else:
            table = "stations_amotekunstation"

        try:
            rows = _fast_knn_station(table, lon, lat, limit)
            # convert geom from text to geojson feature
            for r in rows:
                if r.get("geom"):
                    r["geometry"] = r.pop("geom")
            return Response({"type": "FeatureCollection", "features": rows})
        except Exception as e:
            return Response({"detail": str(e)}, status=500)


class RouteByPgRoutingAPIView(APIView):
    """Scaffolded route endpoint that attempts to call pgr_dijkstra.

    Query params: src_lon, src_lat, dst_lon, dst_lat
    """

    def get(self, request):
        try:
            src_lat = float(request.query_params.get("src_lat"))
            src_lon = float(request.query_params.get("src_lon"))
            dst_lat = float(request.query_params.get("dst_lat"))
            dst_lon = float(request.query_params.get("dst_lon"))
        except Exception:
            return Response(
                {"detail": "Provide src_lat, src_lon, dst_lat, dst_lon"}, status=400
            )

        # This view expects a prepared edge table named 'roads_edges' with columns id, source, target, cost
        sql = (
            "SELECT * FROM pgr_dijkstra("
            "'SELECT id, source, target, cost FROM roads_edges', %s, %s, directed := false)"
        )

        try:
            with connection.cursor() as cur:
                cur.execute(
                    sql, [1, 10]
                )  # placeholder -- user must prepare proper node ids
                cols = [c[0] for c in cur.description] if cur.description else []
                rows = [dict(zip(cols, r)) for r in cur.fetchall()]
            return Response({"route": rows})
        except Exception as e:
            return Response(
                {"detail": "pgRouting call failed or not installed", "error": str(e)},
                status=501,
            )


class PoliceStationListAPIView(APIView):
    """GET /api/stations/police/ - list all police stations"""

    def get(self, request):
        stations = PoliceStation.objects.all()
        serializer = PoliceStationSerializer(stations, many=True)
        return Response(serializer.data)


class AmotekunStationListAPIView(APIView):
    """GET /api/stations/amotekun/ - list all amotekun stations"""

    def get(self, request):
        stations = AmotekunStation.objects.all()
        serializer = AmotekunStationSerializer(stations, many=True)
        return Response(serializer.data)


class HospitalListAPIView(APIView):
    """GET /api/stations/hospitals/ - list all hospitals"""

    def get(self, request):
        hospitals = Hospital.objects.all()
        serializer = HospitalSerializer(hospitals, many=True)
        return Response(serializer.data)
