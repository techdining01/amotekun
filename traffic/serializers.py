from rest_framework import serializers
from .models import TrafficIncident, TrafficFlow, Road, TrafficCamera, TrafficAlert


class TrafficIncidentSerializer(serializers.ModelSerializer):
    reported_by_name = serializers.CharField(source='reported_by.username', read_only=True)
    resolved_by_name = serializers.CharField(source='resolved_by.username', read_only=True)
    
    class Meta:
        model = TrafficIncident
        fields = ['id', 'incident_type', 'severity', 'status', 'location', 'address', 
                  'road_name', 'description', 'affected_lanes', 'estimated_duration',
                  'reported_by', 'reported_by_name', 'reported_at', 'resolved_at', 
                  'resolved_by', 'resolved_by_name']
        read_only_fields = ['reported_at', 'resolved_at']


class TrafficFlowSerializer(serializers.ModelSerializer):
    road_name = serializers.CharField(source='road.name', read_only=True)
    
    class Meta:
        model = TrafficFlow
        fields = ['id', 'road', 'road_name', 'vehicle_count', 'average_speed', 
                  'congestion_level', 'measured_at']
        read_only_fields = ['measured_at']


class RoadSerializer(serializers.ModelSerializer):
    current_flow = serializers.SerializerMethodField()
    
    class Meta:
        model = Road
        fields = ['id', 'name', 'road_type', 'geometry', 'speed_limit', 'lanes', 
                  'capacity', 'is_monitored', 'last_flow_update', 'current_flow',
                  'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    def get_current_flow(self, obj):
        flow = obj.get_current_flow()
        if flow:
            return TrafficFlowSerializer(flow).data
        return None


class TrafficCameraSerializer(serializers.ModelSerializer):
    camera_name = serializers.CharField(source='camera.name', read_only=True)
    camera_status = serializers.CharField(source='camera.status', read_only=True)
    road_name = serializers.CharField(source='monitored_road.name', read_only=True)
    
    class Meta:
        model = TrafficCamera
        fields = ['id', 'camera', 'camera_name', 'camera_status', 'monitored_road', 
                  'road_name', 'direction', 'vehicle_detection_enabled', 
                  'speed_detection_enabled', 'daily_vehicle_count', 'last_count_update']


class TrafficAlertSerializer(serializers.ModelSerializer):
    road_name = serializers.CharField(source='road.name', read_only=True)
    acknowledged_by_name = serializers.CharField(source='acknowledged_by.username', read_only=True)
    
    class Meta:
        model = TrafficAlert
        fields = ['id', 'alert_type', 'severity', 'location', 'road', 'road_name', 
                  'message', 'data', 'acknowledged', 'acknowledged_by', 
                  'acknowledged_by_name', 'acknowledged_at', 'created_at', 'resolved_at']
        read_only_fields = ['created_at', 'resolved_at', 'acknowledged_at']
