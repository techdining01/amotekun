from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from notifications.models import Notification
from .models import Incident


@receiver(post_save, sender=Incident)
def send_incident_notifications(sender, instance, created, **kwargs):
    """Send notifications when a new incident is created."""
    if not created:
        return

    # Get all officers, dispatchers, and admins
    User = settings.AUTH_USER_MODEL
    recipients = User.objects.filter(
        role__in=[
            User.ROLE_CHOICES[1][0],
            User.ROLE_CHOICES[2][0],
            User.ROLE_CHOICES[3][0],
        ]
    )

    # Create a notification for each recipient
    for recipient in recipients:
        Notification.create_notification(
            recipient=recipient,
            notification_type="incident_created",
            title=f"New Incident: {instance.title}",
            message=f"A new {instance.get_report_type_display()} incident has been reported in {instance.lga}, {instance.state}.",
            data={"incident_id": instance.id},
        )
