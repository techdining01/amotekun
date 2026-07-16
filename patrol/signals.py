from django.db.models.signals import (
    post_save,
)

from django.dispatch import receiver

from .models import (
    PatrolMission,
    GPSPosition,
    VehicleAssignment,
    PatrolShift,
)

from .choices import MissionStatus

from .events import mission_created

@receiver(post_save, sender=PatrolMission)
def patrol_created(sender, instance, created, **kwargs):

    if not created:
        return
    mission_created.send(
        sender=PatrolMission, mission=instance,
    )
    

@receiver(post_save, sender=PatrolMission)
def patrol_completed(sender, instance, **kwargs):

    if instance.status != MissionStatus.COMPLETED:
        return
    mission_created.send(sender=PatrolMission, mission=instance)


@receiver(post_save, sender=GPSPosition)
def gps_received(sender, instance, created, **kwargs):

    if not created:

        return


@receiver(post_save, sender=VehicleAssignment)
def vehicle_assigned(sender, instance, created, **kwargs):

    if not created:

        return

@receiver(post_save, sender=PatrolShift)
def shift_started(sender, instance, created, **kwargs):

    if not created:

        return


@receiver(post_save, sender=GPSPosition)

def gps_position_created(sender, instance, created, **kwargs):

    if created:

        gps_received.send(

            sender=GPSPosition,

            gps=instance,

        )