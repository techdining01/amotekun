from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in
from django.utils import timezone

from .models import (
    UserProfile,
    NotificationPreference,
    ResponderStatus,
)
from .choices import AvailabilityStatus

User = get_user_model()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):

    if not created:
        return

    UserProfile.objects.get_or_create(
        user=instance,
    )


@receiver(post_save, sender=User)
def create_notification_preference(sender, instance, created, **kwargs):

    if not created:
        return

    NotificationPreference.objects.get_or_create(
        user=instance,
    )


@receiver(post_save, sender=User)
def create_responder_status(sender, instance, created, **kwargs):

    if not created:
        return

    if not instance.is_superuser:
        ResponderStatus.objects.get_or_create(
            responder=instance,
            defaults={"availability": AvailabilityStatus.OFF_DUTY},
        )


@receiver(user_logged_in)
def update_last_login(sender, user, request, **kwargs):

    user.last_seen = timezone.now()

    user.save(
        update_fields=[
            "last_seen",
        ]
    )

