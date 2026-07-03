from rest_framework import serializers
from .models import Camera, CameraRecording, CameraAlert


class CameraSerializer(serializers.ModelSerializer):
    stream_url = serializers.SerializerMethodField()
    is_online = serializers.SerializerMethodField()

    class Meta:
        model = Camera
        fields = [
            "id",
            "camera_id",
            "mac_address",
            "serial_number",
            "name",
            "description",
            "camera_type",
            "manufacturer",
            "model",
            "location",
            "address",
            "city",
            "state",
            "police_station",
            "amotekun_station",
            "ip_address",
            "port",
            "rtsp_url",
            "hls_url",
            "stream_url",
            "control_url",
            "status",
            "is_online",
            "last_online",
            "last_offline",
            "coverage_radius",
            "viewing_angle",
            "direction",
            "installed_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def get_stream_url(self, obj):
        return obj.get_stream_url()

    def get_is_online(self, obj):
        return obj.is_online()


class CameraRecordingSerializer(serializers.ModelSerializer):
    camera_name = serializers.CharField(source="camera.name", read_only=True)

    class Meta:
        model = CameraRecording
        fields = [
            "id",
            "camera",
            "camera_name",
            "start_time",
            "end_time",
            "duration_seconds",
            "file_path",
            "file_size",
            "is_motion_detected",
            "incident",
            "created_at",
        ]
        read_only_fields = ["created_at"]


class CameraAlertSerializer(serializers.ModelSerializer):
    camera_name = serializers.CharField(source="camera.name", read_only=True)

    class Meta:
        model = CameraAlert
        fields = [
            "id",
            "camera",
            "camera_name",
            "alert_type",
            "severity",
            "message",
            "snapshot_path",
            "video_path",
            "metadata",
            "acknowledged",
            "acknowledged_by",
            "acknowledged_at",
            "incident",
            "created_at",
        ]
        read_only_fields = ["created_at"]
