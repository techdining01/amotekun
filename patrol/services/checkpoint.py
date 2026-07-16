from django.utils import timezone
from patrol.choices import CheckpointStatus



class CheckpointService:

    @staticmethod
    def arrive(checkpoint):

        checkpoint.status = CheckpointStatus.ARRIVED

        checkpoint.arrived_at = timezone.now()

        checkpoint.save()

        return checkpoint

    @staticmethod
    def depart(checkpoint):

        checkpoint.status = CheckpointStatus.DEPARTED

        checkpoint.departed_at = timezone.now()

        checkpoint.save()

        return checkpoint