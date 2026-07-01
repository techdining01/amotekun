from django.db import models
from django.conf import settings
from reports.models import Incident as Report
from stations.models import PoliceStation, AmotekunStation


class Dispatch(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("dispatched", "Dispatched"),
        ("in_progress", "In Progress"),
        ("resolved", "Resolved"),
        ("cancelled", "Cancelled"),
    ]
    
    # Valid status transitions
    VALID_TRANSITIONS = {
        "pending": ["dispatched", "cancelled"],
        "dispatched": ["in_progress", "cancelled"],
        "in_progress": ["resolved", "cancelled"],
        "resolved": [],  # Terminal state
        "cancelled": [],  # Terminal state
    }
    
    incident = models.ForeignKey(
        Report, on_delete=models.CASCADE, related_name="dispatches")
    police_station = models.ForeignKey(
        PoliceStation, on_delete=models.SET_NULL, null=True, blank=True, related_name="dispatches")
    amotekun_station = models.ForeignKey(
        AmotekunStation, on_delete=models.SET_NULL, null=True, blank=True, related_name="dispatches")
    assigned_officer = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, blank=True, 
        limit_choices_to={"role": "OFFICER"},
        related_name="assigned_dispatches")
    assigned_dispatcher = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, blank=True, 
        limit_choices_to={"role": "DISPATCHER"},
        related_name="created_dispatches")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending")
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    dispatched_at = models.DateTimeField(null=True, blank=True)
    in_progress_at = models.DateTimeField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Dispatch for {self.incident.title} - {self.status}"
    
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
    
    def assign_officer(self, officer):
        """Assign an officer to this dispatch"""
        if officer.role != "OFFICER":
            raise ValueError("Can only assign users with OFFICER role")
        
        self.assigned_officer = officer
        if self.status == "pending":
            self.transition_to("dispatched")
        self.save()
        
        # Send notification to officer
        self._send_assignment_notification(officer)
    
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
            if self.assigned_officer:
                notification_service.send_notification(
                    user=self.assigned_officer,
                    notification_type="dispatch_status_changed",
                    title=f"Dispatch Status Updated",
                    message=f"Dispatch for {self.incident.title} changed from {old_status} to {new_status}",
                    data={
                        "dispatch_id": self.id,
                        "incident_id": self.incident.id,
                        "old_status": old_status,
                        "new_status": new_status
                    }
                )
            
            # Notify dispatcher
            if self.assigned_dispatcher:
                notification_service.send_notification(
                    user=self.assigned_dispatcher,
                    notification_type="dispatch_status_changed",
                    title=f"Dispatch Status Updated",
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
    
    def _send_assignment_notification(self, officer):
        """Send notification when officer is assigned"""
        try:
            from notifications.services import notification_service
            
            notification_service.send_notification(
                user=officer,
                notification_type="dispatch_assigned",
                title="New Assignment",
                message=f"You have been assigned to dispatch for {self.incident.title}",
                data={
                    "dispatch_id": self.id,
                    "incident_id": self.incident.id,
                    "incident_title": self.incident.title,
                    "incident_type": self.incident.report_type
                }
            )
        except Exception:
            # Don't break assignment if notification fails
            pass
