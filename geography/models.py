from django.db import models
from django.contrib.gis.db import models as gis_models


class GeographyBoundary(models.Model):
    """Administrative boundaries for geo-spatial queries"""
    STATE_CHOICES = [
        ('Lagos', 'Lagos'),
        ('Ogun', 'Ogun'),
        ('Oyo', 'Oyo'),
        ('Osun', 'Osun'),
        ('Ondo', 'Ondo'),
        ('Ekiti', 'Ekiti'),
    ]
    
    boundary_type = models.CharField(max_length=20, choices=[
        ('state', 'State'),
        ('lga', 'LGA'),
        ('ward', 'Ward'),
        ('custom', 'Custom'),
    ])
    name = models.CharField(max_length=100)
    state_name = models.CharField(max_length=50, blank=True, null=True)
    geometry = gis_models.GeometryField(srid=4326, geography=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['boundary_type']),
        ]

    def __str__(self):
        return f"{self.name} ({self.boundary_type})"