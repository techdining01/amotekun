from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import GeographyBoundary


class GeographyBoundarySerializer(GeoFeatureModelSerializer):
    class Meta:
        model = GeographyBoundary
        geo_field = 'geometry'
        fields = ('id', 'boundary_type', 'name', 'state_name', 'created_at')