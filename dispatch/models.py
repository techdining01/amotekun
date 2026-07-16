from reports.models import Incident 
from django.conf import settings
from django.contrib.gis.db import models
from django.utils import timezone



class Dispatch(models.Model):
 
    # Valid status transitions
    VALID_TRANSITIONS = {
        "pending": ["dispatched", "cancelled"],
        "dispatched": ["in_progress", "cancelled"],
        "in_progress": ["resolved", "cancelled"],
        "resolved": [],  # Terminal state
        "cancelled": [],  # Terminal state
    }
    

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("dispatched", "Dispatched"),
        ("accepted", "Accepted"),
        ("in_progress", "In Progress"),
        ("resolved", "Resolved"),
        ("cancelled", "Cancelled"),
    ]

    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("critical", "Critical"),
    ]


    incident = models.OneToOneField(
        Incident,
        on_delete=models.CASCADE,
        related_name="dispatch",
    )

    reference = models.CharField(
        max_length=30,
        unique=True,
        db_index=True,
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="medium",
        db_index=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        db_index=True,
    )

    dispatcher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="dispatches_managed",
    )

    commander = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="dispatches_authorized",
    )

    patrol_team = models.ForeignKey(
        "patrol.PatrolTeam",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="dispatches",
    )

    vehicle = models.ForeignKey(
        "patrol.Vehicle",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="dispatches",
    )

    mission = models.OneToOneField(
        "patrol.PatrolMission",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="linked_dispatch",
    )

    location = models.PointField(
        srid=4326,
        geography=True,
        null=True,
        blank=True,
    )

    state = models.CharField(
        max_length=100,
        blank=True,
    )

    lga = models.CharField(
        max_length=100,
        blank=True,
    )

    remarks = models.TextField(
        blank=True,
    )

    notes = models.TextField(blank=True, null=True)
    resolution_notes = models.TextField(blank=True, null=True)

    accepted_at = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    dispatched_at = models.DateTimeField(null=True, blank=True)
    in_progress_at = models.DateTimeField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    arrival_at = models.DateTimeField(null=True, blank=True)
    estimated_arrival_time = models.DateTimeField(null=True, blank=True)

    accepted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="accepted_dispatches",
    )

    actual_response_minutes = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["priority"]),
            models.Index(fields=["state"]),
            models.Index(fields=["lga"]),
        ]

    def __str__(self):
        return self.reference

    def save(self, *args, **kwargs):
        if not self.reference:
            timestamp = timezone.now().strftime("%d%m%Y")
            self.reference = f"DISP-{timestamp}-{self.incident_id}"

        super().save(*args, **kwargs)

      
    def can_transition_to(self, new_status):
        """Check if status transition is valid"""
        valid_transitions = self.VALID_TRANSITIONS.get(self.status, [])
        return new_status in valid_transitions
    
    def transition_to(self, new_status):
        """Transition to new status if valid"""
        if not self.can_transition_to(new_status):
            raise ValueError(f"Cannot transition from {self.status} to {new_status}")
        
        old_status = self.status
        self.status = new_status
        
        # Update timestamps based on status
        if new_status == "dispatched":
            from django.utils import timezone
            self.dispatched_at = timezone.now()
        elif new_status == "in_progress":
            from django.utils import timezone
            self.in_progress_at = timezone.now()
        elif new_status == "resolved":
            from django.utils import timezone
            self.resolved_at = timezone.now()
        
        self.save()
        
        # Send notification
        self._send_status_notification(old_status, new_status)
        
        return old_status, new_status
    
    
    def cancel(self, reason=""):
        """Cancel this dispatch"""
        if self.status in ["resolved", "cancelled"]:
            raise ValueError(f"Cannot cancel dispatch in {self.status} status")
        
        old_status, _ = self.transition_to("cancelled")
        if reason:
            self.notes = f"{self.notes}\n\nCancellation reason: {reason}".strip()
            self.save()
        return old_status
    
    def _send_status_notification(self, old_status, new_status):
        """Send notification when dispatch status changes"""
        try:
            from notifications.services import notification_service
            
            # Notify assigned officer
            if self.dispatcher:
                notification_service.send_notification(
                    user=self.dispatcher,
                    notification_type="dispatch_status_changed",
                    title="Dispatch Status Updated",
                    message=f"Dispatch for {self.incident.title} changed from {old_status} to {new_status}",
                    data={
                        "dispatch_id": self.id,
                        "incident_id": self.incident.id,
                        "old_status": old_status,
                        "new_status": new_status
                    }
                )
            
            # Notify patrol team dispatcher
            if self.patrol_team:
                notification_service.send_notification(
                    user=self.patrol_team.dispatcher,
                    notification_type="dispatch_status_changed",
                    title="Dispatch Status Updated",
                    message=f"Dispatch for {self.incident.title} changed from {old_status} to {new_status}",
                    data={
                        "dispatch_id": self.id,
                        "incident_id": self.incident.id,
                        "old_status": old_status,
                        "new_status": new_status
                    }
                )
        except Exception:
            # Don't break dispatch workflow if notification fails
            pass
    
    
class DispatchHistory(models.Model):

    dispatch = models.ForeignKey(
        Dispatch,
        on_delete=models.CASCADE,
        related_name="history",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    action = models.CharField(
        max_length=150,
    )

    note = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.dispatch.reference} - {self.action}"


        