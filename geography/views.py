from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from .models import GeographyBoundary
from .serializers import GeographyBoundarySerializer


class GeographyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GeographyBoundary.objects.all()
    serializer_class = GeographyBoundarySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['get'])
    def nearest(self, request):
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')
        boundary_type = request.query_params.get('type', 'lga')
        limit = int(request.query_params.get('limit', 5))

        if not lat or not lng:
            return Response({'error': 'lat and lng required'}, status=status.HTTP_400_BAD_REQUEST)

        point = Point(float(lng), float(lat), srid=4326)
        boundaries = GeographyBoundary.objects.filter(
            boundary_type=boundary_type
        ).annotate(
            distance=Distance('geometry', point)
        ).order_by('distance')[:limit]

        return Response([{
            'id': b.id,
            'name': b.name,
            'distance_km': b.distance.km
        } for b in boundaries])

    @action(detail=False, methods=['get'])
    def within(self, request):
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')
        radius = float(request.query_params.get('radius', 10))

        if not lat or not lng:
            return Response({'error': 'lat and lng required'}, status=status.HTTP_400_BAD_REQUEST)

        point = Point(float(lng), float(lat), srid=4326)
        boundaries = GeographyBoundary.objects.filter(
            geometry__distance_lte=(point, D(km=radius))
        )
        serializer = self.get_serializer(boundaries, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def buffer(self, request):
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')
        radius = float(request.query_params.get('radius', 1))

        if not lat or not lng:
            return Response({'error': 'lat and lng required'}, status=status.HTTP_400_BAD_REQUEST)

        point = Point(float(lng), float(lat), srid=4326)
        buffer = point.buffer(radius * 1000)
        boundaries = GeographyBoundary.objects.filter(
            geometry__intersects=buffer
        )
        return Response({'buffer_intersects': GeographyBoundarySerializer(boundaries, many=True).data})