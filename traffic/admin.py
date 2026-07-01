from django.contrib import admin
from django.contrib.gis.forms import OSMWidget
from django import forms
from .models import TrafficIncident, TrafficFlow, Road, TrafficCamera, TrafficAlert

class TrafficIncidentForm(forms.ModelForm):
    class Meta:
        model = TrafficIncident
        fields = '__all__'
        widgets = {
            'location': OSMWidget(attrs={'default_lon': 8.675, 'default_lat': 9.082, 'default_zoom': 6}),
        }

class RoadForm(forms.ModelForm):
    class Meta:
        model = Road
        fields = '__all__'
        widgets = {
            'geometry': OSMWidget(attrs={'default_lon': 8.675, 'default_lat': 9.082, 'default_zoom': 6}),
        }

class TrafficAlertForm(forms.ModelForm):
    class Meta:
        model = TrafficAlert
        fields = '__all__'
        widgets = {
            'location': OSMWidget(attrs={'default_lon': 8.675, 'default_lat': 9.082, 'default_zoom': 6}),
        }


@admin.register(TrafficIncident)
class TrafficIncidentAdmin(admin.ModelAdmin):
    form = TrafficIncidentForm
    list_display = ['incident_type', 'severity', 'status', 'road_name', 'reported_at', 'resolved_at']
    list_filter = ['incident_type', 'severity', 'status', 'reported_at']
    search_fields = ['road_name', 'address', 'description']
    readonly_fields = ['reported_at', 'resolved_at']


@admin.register(TrafficFlow)
class TrafficFlowAdmin(admin.ModelAdmin):
    list_display = ['road', 'vehicle_count', 'average_speed', 'congestion_level', 'measured_at']
    list_filter = ['congestion_level', 'measured_at']
    search_fields = ['road__name']
    readonly_fields = ['measured_at']


@admin.register(Road)
class RoadAdmin(admin.ModelAdmin):
    form = RoadForm
    list_display = ['name', 'road_type', 'speed_limit', 'lanes', 'is_monitored', 'last_flow_update']
    list_filter = ['road_type', 'is_monitored']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(TrafficCamera)
class TrafficCameraAdmin(admin.ModelAdmin):
    list_display = ['camera', 'monitored_road', 'direction', 'vehicle_detection_enabled', 'daily_vehicle_count']
    list_filter = ['vehicle_detection_enabled', 'speed_detection_enabled']
    search_fields = ['camera__name', 'monitored_road__name']


@admin.register(TrafficAlert)
class TrafficAlertAdmin(admin.ModelAdmin):
    form = TrafficAlertForm
    list_display = ['alert_type', 'severity', 'road', 'acknowledged', 'created_at', 'resolved_at']
    list_filter = ['alert_type', 'severity', 'acknowledged', 'created_at']
    search_fields = ['road__name', 'message']
    readonly_fields = ['created_at', 'resolved_at', 'acknowledged_at']
