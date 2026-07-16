from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from django.contrib.auth import get_user_model
from .models import MobileDevice, PushNotification
from reports.models import Incident, IncidentMedia
from stations.models import PoliceStation, AmotekunStation, Hospital

User = get_user_model()


class MobileDeviceSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = MobileDevice
        fields = ['id', 'user', 'user_name', 'device_type', 'device_id', 'fcm_token',
                  'app_version', 'os_version', 'device_name', 'is_active', 
                  'last_used', 'registered_at']
        read_only_fields = ['registered_at', 'last_used']


class PushNotificationSerializer(serializers.ModelSerializer):
    recipient_name = serializers.CharField(source='recipient.username', read_only=True)
    
    class Meta:
        model = PushNotification
        fields = ['id', 'recipient', 'recipient_name', 'device', 'title', 'body', 
                  'data', 'status', 'error_message', 'created_at', 'sent_at']
        read_only_fields = ['created_at', 'sent_at', 'status']


class DeviceRegistrationSerializer(serializers.Serializer):
    device_type = serializers.ChoiceField(choices=['ios', 'android'])
    device_id = serializers.CharField(max_length=255)
    fcm_token = serializers.CharField(max_length=500)
    app_version = serializers.CharField(max_length=50, required=False)
    os_version = serializers.CharField(max_length=50, required=False)
    device_name = serializers.CharField(max_length=255, required=False)


class MobileIncidentSerializer(GeoFeatureModelSerializer):
    lat = serializers.FloatField(write_only=True, required=False)
    lng = serializers.FloatField(write_only=True, required=False)

    class Meta:
        model = Incident
        geo_field = 'geometry'
        fields = ('id', 'title', 'description', 'report_type', 'state', 'lga', 
                  'lat', 'lng', 'created_at')
        read_only_fields = ('id', 'state', 'lga', 'created_at')


class FacilitySerializer(GeoFeatureModelSerializer):
    facility_type = serializers.SerializerMethodField()
    distance = serializers.FloatField(required=False, read_only=True)

    class Meta:
        model = PoliceStation
        fields = ('id', 'name', 'address', 'state', 'lga', 'facility_type', 'distance')
        geo_field = 'location'

    def get_facility_type(self, obj):
        return 'police_station'


class AmotekunFacilitySerializer(GeoFeatureModelSerializer):
    facility_type = serializers.SerializerMethodField()

    class Meta:
        model = AmotekunStation
        fields = ('id', 'name', 'address', 'state', 'lga', 'facility_type')
        geo_field = 'location'

    def get_facility_type(self, obj):
        return 'amotekun_station'


class HospitalSerializer(GeoFeatureModelSerializer):
    facility_type = serializers.SerializerMethodField()

    class Meta:
        model = Hospital
        fields = ('id', 'name', 'address', 'state', 'lga', 'has_emergency', 'facility_type')
        geo_field = 'location'

    def get_facility_type(self, obj):
        return 'hospital'


class MediaUploadSerializer(serializers.Serializer):
    media_type = serializers.ChoiceField(choices=Incident.MEDIA_TYPES)
    file = serializers.FileField(required=False)
    caption = serializers.CharField(required=False, allow_blank=True, max_length=500)


class IncidentMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncidentMedia
        fields = ('id', 'incident', 'media_type', 'file', 'caption', 'uploaded_at')
        read_only_fields = ('id', 'uploaded_at')
