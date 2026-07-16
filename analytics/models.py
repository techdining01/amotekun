from django.contrib.gis.db import models 
from django.contrib.gis.geos import Point


class Hotspot(models.Model):
    HOTSPOT_TYPES = [
        ('crime', 'Crime'),
        ('violence', 'Violence'),
        ('traffic', 'Traffic'),
    ]
    
    location = models.PointField(srid=4326, geography=True)
    hotspot_type = models.CharField(max_length=20, choices=HOTSPOT_TYPES, default='crime')
    intensity_score = models.FloatField(help_text='0-1 scale indicating hotspot intensity')
    incident_count = models.IntegerField(default=0)
    calculated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['hotspot_type', '-intensity_score']),
            models.Index(fields=['-calculated_at']),
        ]
        ordering = ['-intensity_score']

    def __str__(self):
        return f"{self.hotspot_type} hotspot - intensity: {self.intensity_score:.2f}"


class HotspotAnalysis(models.Model):
    analysis_type = models.CharField(max_length=50)
    parameters = models.JSONField(default=dict)
    hotspot_bounds = models.PolygonField(srid=4326, geography=True, null=True, blank=True)
    results = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.analysis_type} - {self.created_at}"