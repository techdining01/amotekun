from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Hotspot, HotspotAnalysis


class HotspotSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Hotspot
        geo_field = 'location'
        fields = ('id', 'hotspot_type', 'intensity_score', 'incident_count', 'calculated_at')


class HotspotAnalysisSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = HotspotAnalysis
        geo_field = 'hotspot_bounds'
        fields = ('id', 'analysis_type', 'parameters', 'results', 'created_at', 'completed_at')