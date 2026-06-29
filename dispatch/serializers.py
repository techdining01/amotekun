from rest_framework import serializers
from .models import Dispatch


class DispatchSerializer(serializers.ModelSerializer):
    incident_title = serializers.CharField(source='incident.title', read_only=True)
    assigned_officer_name = serializers.CharField(source='assigned_officer.username', read_only=True)
    assigned_dispatcher_name = serializers.CharField(source='assigned_dispatcher.username', read_only=True)
    police_station_name = serializers.CharField(source='police_station.name', read_only=True)
    amotekun_station_name = serializers.CharField(source='amotekun_station.name', read_only=True)
    
    class Meta:
        model = Dispatch
        fields = "__all__"
        read_only_fields = ['assigned_dispatcher', 'created_at', 'updated_at']
