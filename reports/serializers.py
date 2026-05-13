from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import Reports


class ReportsSerializer(GeoFeatureModelSerializer):

    class meta:
        model = Reports

        geo_field = 'location'

        fields = '__all__'

