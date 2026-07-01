from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.db.models import Count
from django.contrib.gis.db.models.functions import Centroid
from .models import Hotspot, HotspotAnalysis
from .serializers import HotspotSerializer, HotspotAnalysisSerializer
from reports.models import Incident


class HotspotViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Hotspot.objects.all()
    serializer_class = HotspotSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['get'])
    def crime(self, request):
        """Get top crime hotspots"""
        hotspots = Hotspot.objects.filter(hotspot_type='crime').order_by('-intensity_score')[:50]
        return Response(self.get_serializer(hotspots, many=True).data)

    @action(detail=False, methods=['post'])
    def generate(self, request):
        """Generate hotspots from incidents using grid-based clustering"""
        lat = request.data.get('lat')
        lng = request.data.get('lng')
        radius_km = float(request.data.get('radius', 10))
        grid_size = float(request.data.get('grid_size', 0.01))

        if lat and lng:
            point = Point(float(lng), float(lat), srid=4326)
            incidents = Incident.objects.filter(
                geometry__distance_lte=(point, D(km=radius_km))
            )
        else:
            incidents = Incident.objects.all()

        hotspots = []
        if incidents.exists():
            from django.contrib.gis.db.models.functions import GeoHash
            from collections import defaultdict
            import math
            
            grid_counts = defaultdict(int)
            for incident in incidents:
                lat_grid = int(incident.geometry.y / grid_size)
                lng_grid = int(incident.geometry.x / grid_size)
                grid_counts[(lat_grid, lng_grid)] += 1

            for (lat_grid, lng_grid), count in sorted(grid_counts.items(), key=lambda x: -x[1])[:100]:
                center_lat = (lat_grid + 0.5) * grid_size
                center_lng = (lng_grid + 0.5) * grid_size
                center_point = Point(center_lng, center_lat, srid=4326)
                
                intensity = min(1.0, count / 10.0)
                hotspot = Hotspot.objects.create(
                    location=center_point,
                    hotspot_type='crime',
                    intensity_score=intensity,
                    incident_count=count
                )
                hotspots.append(hotspot)

        HotspotAnalysis.objects.create(
            analysis_type='crime_hotspot',
            parameters={'radius_km': radius_km, 'grid_size': grid_size},
            hotspot_bounds=incidents[0].geometry.convex_hull if incidents.exists() else None,
            results={'hotspot_count': len(hotspots)}
        )

        return Response({'generated': len(hotspots)})


class HotspotAnalysisViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HotspotAnalysis.objects.all()
    serializer_class = HotspotAnalysisSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]