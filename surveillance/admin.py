from django.contrib import admin
from .models import Camera, CameraRecording, CameraAlert


@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin):
    list_display = ['name', 'camera_id', 'camera_type', 'status', 'ip_address', 'last_online']
    list_filter = ['status', 'camera_type', 'city', 'state']
    search_fields = ['name', 'camera_id', 'mac_address', 'serial_number', 'address']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Identification', {
            'fields': ('camera_id', 'mac_address', 'serial_number')
        }),
        ('Basic Information', {
            'fields': ('name', 'description', 'camera_type', 'manufacturer', 'model')
        }),
        ('Location', {
            'fields': ('location', 'address', 'city', 'state')
        }),
        ('Station Association', {
            'fields': ('police_station', 'amotekun_station')
        }),
        ('Connection', {
            'fields': ('ip_address', 'port', 'rtsp_url', 'hls_url', 'username', 'password')
        }),
        ('Status', {
            'fields': ('status', 'last_online', 'last_offline')
        }),
        ('Coverage', {
            'fields': ('coverage_radius', 'viewing_angle', 'direction')
        }),
        ('Timestamps', {
            'fields': ('installed_at', 'created_at', 'updated_at')
        }),
    )


@admin.register(CameraRecording)
class CameraRecordingAdmin(admin.ModelAdmin):
    list_display = ['camera', 'start_time', 'end_time', 'duration_seconds', 'is_motion_detected']
    list_filter = ['is_motion_detected', 'start_time']
    search_fields = ['camera__name', 'file_path']
    readonly_fields = ['created_at']


@admin.register(CameraAlert)
class CameraAlertAdmin(admin.ModelAdmin):
    list_display = ['camera', 'alert_type', 'severity', 'acknowledged', 'created_at']
    list_filter = ['alert_type', 'severity', 'acknowledged', 'created_at']
    search_fields = ['camera__name', 'message']
    readonly_fields = ['created_at']
