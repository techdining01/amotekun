from django.db import models
from django.contrib.gis.db import models as gis_models
from django.conf import settings


class TrafficIncident(models.Model):
    """Traffic-related incidents (accidents, congestion, road closures)"""

    INCIDENT_TYPES = [
        ("accident", "Accident"),
        ("congestion", "Congestion"),
        ("road_closure", "Road Closure"),
        ("construction", "Construction"),
        ("weather", "Weather Related"),
        ("event", "Special Event"),
    ]

    SEVERITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("critical", "Critical"),
    ]

    STATUS_CHOICES = [
        ("active", "Active"),
        ("resolved", "Resolved"),
        ("monitoring", "Monitoring"),
    ]

    incident_type = models.CharField(max_length=50, choices=INCIDENT_TYPES)
    severity = models.CharField(
        max_length=20, choices=SEVERITY_CHOICES, default="medium"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")

    # Location
    location = gis_models.PointField(srid=4326)
    address = models.CharField(max_length=255, blank=True)
    road_name = models.CharField(max_length=255, blank=True)

    # Details
    description = models.TextField(blank=True)
    affected_lanes = models.IntegerField(
        default=1, help_text="Number of affected lanes"
    )
    estimated_duration = models.IntegerField(
        null=True, blank=True, help_text="Duration in minutes"
    )

    # Reporting
    reported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reported_traffic_incidents",
    )
    reported_at = models.DateTimeField(auto_now_add=True)

    # Resolution
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="resolved_traffic_incidents",
    )

    class Meta:
        ordering = ["-reported_at"]
        indexes = [
            models.Index(fields=["status", "-reported_at"]),
            models.Index(fields=["severity", "-reported_at"]),
            models.Index(fields=["location"]),
        ]

    def __str__(self):
        return f"{self.incident_type} - {self.road_name or 'Unknown location'}"


class TrafficFlow(models.Model):
    """Traffic flow measurements for roads/segments"""

    road = models.ForeignKey(
        "Road", on_delete=models.CASCADE, related_name="traffic_flows"
    )

    # Flow measurements
    vehicle_count = models.IntegerField(default=0)
    average_speed = models.FloatField(help_text="Average speed in km/h")
    congestion_level = models.CharField(
        max_length=20,
        choices=[
            ("free", "Free Flow"),
            ("moderate", "Moderate"),
            ("heavy", "Heavy"),
            ("severe", "Severe"),
        ],
        default="free",
    )

    # Timestamp
    measured_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-measured_at"]
        indexes = [
            models.Index(fields=["road", "-measured_at"]),
            models.Index(fields=["congestion_level", "-measured_at"]),
        ]

    def __str__(self):
        return f"{self.road.name} - {self.congestion_level}"


class Road(models.Model):
    """Road segments for traffic monitoring"""

    ROAD_TYPES = [
        ("highway", "Highway"),
        ("arterial", "Arterial"),
        ("collector", "Collector"),
        ("local", "Local"),
    ]

    source_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    road_type = models.CharField(max_length=20, choices=ROAD_TYPES, default="local")
    geometry = gis_models.LineStringField(srid=4326, null=True, blank=True)

    # Traffic capacity
    speed_limit = models.IntegerField(help_text="Speed limit in km/h", null=True, blank=True)
    lanes = models.IntegerField(default=2)
    capacity = models.IntegerField(help_text="Vehicles per hour", null=True, blank=True)

    # Monitoring
    is_monitored = models.BooleanField(default=True)
    last_flow_update = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["is_monitored"]),
            models.Index(fields=["road_type"]),
            models.Index(fields=["source_id"]),
        ]

    def __str__(self):
        return f"{self.name or 'Unnamed road'} {self.road_type} {self.speed_limit if self.speed_limit else 'N/A'} km/h"

    def get_current_flow(self):
        """Get most recent traffic flow data"""
        return self.traffic_flows.first()


class TrafficSnapshot(models.Model):
    """Historical traffic provider snapshot for later intelligence."""

    provider = models.CharField(max_length=100)
    road = models.ForeignKey(
        Road, on_delete=models.SET_NULL, null=True, blank=True, related_name="snapshots"
    )
    road_name = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField()
    average_speed = models.FloatField(null=True, blank=True)
    travel_time = models.FloatField(
        null=True, blank=True, help_text="Seconds or minutes depending on provider"
    )
    congestion_level = models.CharField(
        max_length=50,
        choices=[
            ("free", "Free Flow"),
            ("moderate", "Moderate"),
            ("heavy", "Heavy"),
            ("severe", "Severe"),
            ("unknown", "Unknown"),
        ],
        default="unknown",
    )
    geometry = gis_models.LineStringField(srid=4326, null=True, blank=True)
    incident_count = models.IntegerField(default=0)
    camera_count = models.IntegerField(default=0)
    weather_condition = models.CharField(max_length=100, blank=True)
    raw_data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["provider", "timestamp"]),
            models.Index(fields=["congestion_level", "-timestamp"]),
            models.Index(fields=["road", "-timestamp"]),
        ]

    def __str__(self):
        return f"{self.provider} @ {self.timestamp.isoformat()} - {self.road_name or 'Unknown'}"


class TrafficCamera(models.Model):
    """Traffic monitoring cameras"""

    camera = models.OneToOneField(
        "surveillance.Camera", on_delete=models.CASCADE, related_name="traffic_data"
    )

    # Traffic-specific data
    monitored_road = models.ForeignKey(
        Road, on_delete=models.SET_NULL, null=True, blank=True
    )
    direction = models.CharField(
        max_length=50, blank=True, help_text="e.g., Northbound"
    )

    # Detection settings
    vehicle_detection_enabled = models.BooleanField(default=True)
    speed_detection_enabled = models.BooleanField(default=False)

    # Statistics
    daily_vehicle_count = models.IntegerField(default=0)
    last_count_update = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["camera__name"]

    def __str__(self):
        return f"Traffic Camera - {self.camera.name}"


class TrafficAlert(models.Model):
    """Alerts generated from traffic monitoring"""

    ALERT_TYPES = [
        ("congestion", "Congestion Alert"),
        ("accident", "Accident Detected"),
        ("abnormal_speed", "Abnormal Speed"),
        ("road_closure", "Road Closure"),
        ("weather", "Weather Impact"),
    ]

    alert_type = models.CharField(max_length=50, choices=ALERT_TYPES)
    severity = models.CharField(
        max_length=20,
        choices=[
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
            ("critical", "Critical"),
        ],
        default="medium",
    )

    # Location
    location = gis_models.PointField(srid=4326)
    road = models.ForeignKey(Road, on_delete=models.SET_NULL, null=True, blank=True)

    # Details
    message = models.TextField()
    data = models.JSONField(default=dict, blank=True)

    # Status
    acknowledged = models.BooleanField(default=False)
    acknowledged_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    acknowledged_at = models.DateTimeField(null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["alert_type", "-created_at"]),
            models.Index(fields=["severity", "-created_at"]),
            models.Index(fields=["acknowledged"]),
        ]

    def __str__(self):
        return f"{self.alert_type} - {self.road.name if self.road else 'Unknown road'}"
