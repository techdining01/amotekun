import requests
from django.db import models
from django.conf import settings
from django.contrib.gis.db import models as gis_models
from cryptography.fernet import Fernet
import base64


class Camera(models.Model):
    """CCTV Camera model with identification via MAC address or camera ID"""

    CAMERA_TYPES = [
        ("fixed", "Fixed"),
        ("ptz", "PTZ (Pan-Tilt-Zoom)"),
        ("dome", "Dome"),
        ("bullet", "Bullet"),
        ("thermal", "Thermal"),
    ]

    STATUS_CHOICES = [
        ("online", "Online"),
        ("offline", "Offline"),
        ("maintenance", "Under Maintenance"),
        ("error", "Error"),
    ]

    # Identification
    camera_id = models.CharField(
        max_length=100, unique=True, help_text="Unique camera identifier"
    )
    mac_address = models.CharField(
        max_length=17,
        unique=True,
        null=True,
        blank=True,
        help_text="MAC address (e.g., 00:1A:2B:3C:4D:5E)",
    )
    serial_number = models.CharField(max_length=100, unique=True, null=True, blank=True)

    # Basic info
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    camera_type = models.CharField(max_length=20, choices=CAMERA_TYPES, default="fixed")
    manufacturer = models.CharField(max_length=100, blank=True)
    model = models.CharField(max_length=100, blank=True)

    # Location
    location = gis_models.PointField(
        srid=4326,
        geography=True,
        help_text="Camera GPS coordinates",
        null=True,
        blank=True,
    )
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)

    # Station association
    police_station = models.ForeignKey(
        "stations.PoliceStation",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cameras",
    )
    amotekun_station = models.ForeignKey(
        "stations.AmotekunStation",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cameras",
    )

    # Connection info
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    port = models.IntegerField(default=80)
    rtsp_url = models.URLField(max_length=500, blank=True, help_text="RTSP stream URL")
    hls_url = models.URLField(max_length=500, blank=True, help_text="HLS stream URL")
    control_url = models.URLField(
        max_length=500, blank=True, help_text="Optional PTZ control API endpoint"
    )
    username = models.CharField(max_length=100, blank=True)
    password = models.CharField(
        max_length=255, blank=True, help_text="Encrypted at rest"
    )

    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="offline")
    last_online = models.DateTimeField(null=True, blank=True)
    last_offline = models.DateTimeField(null=True, blank=True)

    # Coverage area
    coverage_radius = models.FloatField(
        default=100, help_text="Coverage radius in meters"
    )
    viewing_angle = models.FloatField(default=90, help_text="Viewing angle in degrees")
    direction = models.FloatField(
        default=0, help_text="Direction in degrees (0 = North)"
    )

    # Timestamps
    installed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["camera_id"]),
            models.Index(fields=["mac_address"]),
            models.Index(fields=["status"]),
            models.Index(fields=["location"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.camera_id})"

    def get_stream_url(self):
        """Get the primary stream URL"""
        return self.hls_url or self.rtsp_url

    def get_ptz_control_url(self):
        """Get the configured PTZ control endpoint."""
        return self.control_url or ""

    def is_online(self):
        """Check if camera is currently online"""
        return self.status == "online"

    def send_ptz_command(self, action, speed=1, preset=None):
        """Send a PTZ command to the camera control endpoint."""
        url = self.get_ptz_control_url()
        if not url:
            raise RuntimeError("PTZ control URL is not configured for this camera.")

        payload = {"action": action, "speed": speed}
        if preset is not None:
            payload["preset"] = preset

        auth = None
        if self.username:
            password = self.get_password()
            if password:
                auth = (self.username, password)

        response = requests.post(url, json=payload, auth=auth, timeout=10)
        response.raise_for_status()

        try:
            return response.json()
        except ValueError:
            return {"status": "ok", "http_status": response.status_code}

    def mark_offline(self):
        """Mark camera as offline"""
        from django.utils import timezone

        self.status = "offline"
        self.last_offline = timezone.now()
        self.save()

    def set_password(self, raw_password):
        """Encrypt and set camera password"""
        if not raw_password:
            self.password = ""
            return

        # Ensure encryption key exists
        camera_encryption_key = getattr(settings, "CAMERA_ENCRYPTION_KEY", None)
        if not camera_encryption_key:
            # Fallback to SECRET_KEY if CAMERA_ENCRYPTION_KEY not set
            camera_encryption_key = settings.SECRET_KEY

        # Ensure key is valid for Fernet (32 bytes, base64 encoded)
        if (
            len(camera_encryption_key) != 44
        ):  # Fernet keys are 44 characters when base64 encoded
            # Derive a proper key from the SECRET_KEY
            from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
            from cryptography.hazmat.primitives import hashes

            salt = b"amotekun_camera_encryption"  # Fixed salt for consistency
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(camera_encryption_key.encode()))
            fernet = Fernet(key)
        else:
            fernet = Fernet(camera_encryption_key.encode())

        self.password = fernet.encrypt(raw_password.encode()).decode()

    def get_password(self):
        """Decrypt and return camera password"""
        if not self.password:
            return ""

        # Ensure encryption key exists
        camera_encryption_key = getattr(settings, "CAMERA_ENCRYPTION_KEY", None)
        if not camera_encryption_key:
            # Fallback to SECRET_KEY if CAMERA_ENCRYPTION_KEY not set
            camera_encryption_key = settings.SECRET_KEY

        # Ensure key is valid for Fernet
        if len(camera_encryption_key) != 44:
            # Derive the same key as in set_password
            from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
            from cryptography.hazmat.primitives import hashes

            salt = b"amotekun_camera_encryption"
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(camera_encryption_key.encode()))
            fernet = Fernet(key)
        else:
            fernet = Fernet(camera_encryption_key.encode())

        try:
            return fernet.decrypt(self.password.encode()).decode()
        except Exception:
            # If decryption fails, return empty string
            return ""


class CameraRecording(models.Model):
    """Camera recording/session"""

    camera = models.ForeignKey(
        Camera, on_delete=models.CASCADE, related_name="recordings"
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.IntegerField(null=True, blank=True)
    file_path = models.CharField(max_length=500, blank=True)
    file_size = models.BigIntegerField(null=True, blank=True)
    is_motion_detected = models.BooleanField(default=False)
    incident = models.ForeignKey(
        "reports.Incident",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="camera_recordings",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-start_time"]
        indexes = [
            models.Index(fields=["camera", "-start_time"]),
            models.Index(fields=["incident"]),
        ]

    def __str__(self):
        return f"{self.camera.name} - {self.start_time}"


class CameraAlert(models.Model):
    """Alert generated by camera (motion detection, etc.)"""

    ALERT_TYPES = [
        ("motion", "Motion Detected"),
        ("intrusion", "Intrusion Detected"),
        ("object_left", "Object Left Behind"),
        ("face_detected", "Face Detected"),
        ("license_plate", "License Plate Detected"),
        ("offline", "Camera Offline"),
        ("error", "Camera Error"),
    ]

    SEVERITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("critical", "Critical"),
    ]

    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, related_name="alerts")
    alert_type = models.CharField(max_length=50, choices=ALERT_TYPES)
    severity = models.CharField(
        max_length=20, choices=SEVERITY_CHOICES, default="medium"
    )
    message = models.TextField()
    snapshot_path = models.CharField(max_length=500, blank=True)
    video_path = models.CharField(max_length=500, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    acknowledged = models.BooleanField(default=False)
    acknowledged_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="acknowledged_camera_alerts",
    )
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    incident = models.ForeignKey(
        "reports.Incident",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="camera_alerts",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["camera", "-created_at"]),
            models.Index(fields=["severity", "-created_at"]),
            models.Index(fields=["acknowledged"]),
        ]

    def __str__(self):
        return f"{self.camera.name} - {self.alert_type} ({self.severity})"

    def acknowledge(self, user):
        """Acknowledge the alert"""
        from django.utils import timezone

        self.acknowledged = True
        self.acknowledged_by = user
        self.acknowledged_at = timezone.now()
        self.save()
