from django.contrib import admin
from .models import Hotspot, HotspotAnalysis


@admin.register(Hotspot)
class HotspotAdmin(admin.ModelAdmin):
    list_display = ['hotspot_type', 'intensity_score', 'incident_count', 'calculated_at']
    list_filter = ['hotspot_type', 'calculated_at']
    readonly_fields = ['calculated_at']


@admin.register(HotspotAnalysis)
class HotspotAnalysisAdmin(admin.ModelAdmin):
    list_display = ['analysis_type', 'created_at', 'completed_at']
    list_filter = ['analysis_type', 'created_at']
    readonly_fields = ['created_at']
