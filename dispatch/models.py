from django.db import models
from django.contrib.gis.db import models as gis_models
from reports.models import Incident
from stations.models import PoliceStation, AmotekunStation


class Dispatch(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("dispatched", "Dispatched"),
        ("in_progress", "In Progress"),
        ("resolved", "Resolved"),
        ("cancelled", "Cancelled"),
    ]
    
    incident = models.ForeignKey(
        Incident, on_delete=models.CASCADE, related_name="dispatches")
    police_station = models.ForeignKey(
        PoliceStation, on_delete=models.SET_NULL, null=True, blank=True, related_name="dispatches")
    amotekun_station = models.ForeignKey(
        AmotekunStation, on_delete=models.SET_NULL, null=True, blank=True, related_name="dispatches")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending")
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Dispatch for {self.incident.title} - {self.status}"
