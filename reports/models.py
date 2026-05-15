from django.contrib.gis.db import models


class Incident(models.Model):
    REPORT_TYPES = [
        ("crime", "Crime"),
        ("violence", "Violence"),
        ("fire", "Fire"),
        ("flood", "Flood"),
        ("accident", "Accident"),
    ]

    title = models.CharField(max_length=50)
    description = models.TextField()
    report_type = models.CharField(max_length=50, choices=REPORT_TYPES)
    geometry = models.PointField()
    state = models.CharField(max_length=70)
    lga = models.CharField(max_length=70)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class FloodZone(models.Model):
    name = models.CharField(max_length=100)
    geometry = models.PolygonField()
    risk_level = models.CharField

    def __str__(self):
        return self.name


class CrimeHotspot(models.Model):
    name = models.CharField(max_length=255)
    geometry = models.PolygonField()
    severity = models.IntegerField(default=1)

    def __str__(self):
        return f" {self.name}: {self.severity}"


class Road(models.Model):
    name = models.CharField
    geometry = models.LineStringField()

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=100)
    geometry = models.PolygonField()

    def __str__(self):
        return self.name


class LGA(models.Model):
    state = models.ForeignKey(
        State, on_delete=models.CASCADE, related_name="lgas", null=True, blank=True
    )
    name = models.CharField(max_length=100)

    geometry = models.MultiPolygonField()

    def __str__(self):
        return self.name
