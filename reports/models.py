from django.db import models
from django.contrib.gis.db import models as gis_models
from django.conf import settings


class Incident(models.Model):
    REPORT_TYPES = [
        ("crime", "Crime"),
        ("violence", "Violence"),
        ("fire", "Fire"),
        ("flood", "Flood"),
        ("accident", "Accident"),
    ]

    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reported_incidents",
    )
    title = models.CharField(max_length=50)
    description = models.TextField()
    report_type = models.CharField(max_length=50, choices=REPORT_TYPES)
    geometry = gis_models.PointField(srid=4326, geography=True)
    state = models.CharField(max_length=70)
    lga = models.CharField(max_length=70)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class IncidentMedia(models.Model):
    MEDIA_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name='media')
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES)
    file = models.FileField(upload_to='incidents/%d/%m/%Y/')
    caption = models.CharField(max_length=500, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.media_type} for {self.incident.title}"


class FloodZone(models.Model):
    name = models.CharField(max_length=100)
    geometry = gis_models.PointField(srid=4326, geography=True)
    risk_level = models.CharField(
        max_length=50,
        choices=[("low", "Low"), ("medium", "Medium"), ("high", "High")],
        default="low",
    )

    def __str__(self):
        return self.name


class CrimeHotspot(models.Model):
    name = models.CharField(max_length=255)
    geometry = gis_models.PointField(srid=4326, geography=True)
    severity = models.IntegerField(default=1)

    def __str__(self):
        return f" {self.name}: {self.severity}"


class Road(models.Model):
    name = models.CharField(max_length=255)
    geometry = gis_models.LineStringField(srid=4326, geography=True)

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=100)
    geometry = gis_models.MultiPolygonField(srid=4326, geography=True)

    def __str__(self):
        return self.name


class LGA(models.Model):
    state = models.ForeignKey(
        State, on_delete=models.CASCADE, related_name="lgas", null=True, blank=True
    )
    name = models.CharField(max_length=100)

    geometry = gis_models.MultiPolygonField(srid=4326, null=True, blank=True)

    def __str__(self):
        return self.name



class Ward(models.Model):
    lga = models.ForeignKey(LGA, on_delete=models.CASCADE, related_name="wards")

    name = models.CharField(max_length=150)

    geometry = gis_models.GeometryField(srid=4326)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (
            "lga",
            "name",
        )

    def __str__(self):
        return self.name
