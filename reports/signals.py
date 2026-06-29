from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Incident


@receiver(post_save, sender=Incident)
def send_incident_notification(sender, instance, created, **kwargs):
    """
    Send notification to dispatchers when a new incident is created
    """
    if created:
        try:
            from notifications.services import notification_service
            notification_service.send_to_role(
                role='DISPATCHER',
                notification_type='incident_created',
                title='New Incident Reported',
                message=f'New incident: {instance.title} ({instance.report_type})',
                data={
                    'incident_id': instance.id,
                    'title': instance.title,
                    'report_type': instance.report_type,
                    'location': {
                        'lat': instance.geometry.y,
                        'lng': instance.geometry.x
                    }
                }
            )
        except Exception:
            # Don't break incident creation if notification fails
            pass
