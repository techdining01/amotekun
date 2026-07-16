from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Incident


@receiver(post_save, sender=Incident)
def send_incident_notifications(sender, instance, created, **kwargs):
    if not created:
        return

    User = get_user_model()
    recipients = User.objects.filter(
        role__in=[
            'PATROL_OFFICER', 'PATROL_SUPERVISOR', 'DISPATCHER',
            'EMERGENCY_OPERATOR', 'RESPONDER', 'STATE_COMMANDER',
            'LGA_COMMANDER', 'STATION_COMMANDER', 'PLATFORM_ADMIN', 'SUPER_ADMIN',
        ]
    )

    try:
        from notifications.services import NotificationService
        svc = NotificationService()
        for recipient in recipients:
            svc.send_notification(
                user=recipient,
                notification_type="incident_created",
                title=f"New Incident: {instance.title}",
                message=f"A new {instance.get_report_type_display()} incident has been reported in {instance.lga}, {instance.state}.",
                data={"incident_id": instance.id, "report_type": instance.report_type},
            )
    except Exception:
        # Fallback: store without real-time push
        from notifications.models import Notification
        for recipient in recipients:
            Notification.create_notification(
                recipient=recipient,
                notification_type="incident_created",
                title=f"New Incident: {instance.title}",
                message=f"A new {instance.get_report_type_display()} incident has been reported in {instance.lga}, {instance.state}.",
                data={"incident_id": instance.id, "report_type": instance.report_type},
            )
