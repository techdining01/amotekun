from django.db import transaction
from django.utils import timezone
from ..models import VehicleAssignment, VehicleStatus



class VehicleAssignmentService:

    @staticmethod
    @transaction.atomic
    def assign(
        vehicle,
        patrol_team,
    ):

        VehicleAssignment.objects.filter(
            patrol_team=patrol_team,
            active=True,
        ).update(
            active=False,
            released_at=timezone.now(),
        )

        assignment = VehicleAssignment.objects.create(

            vehicle=vehicle,

            patrol_team=patrol_team,

        )

        vehicle.status = VehicleStatus.ASSIGNED

        vehicle.save(
            update_fields=[
                "status",
            ]
        )

        return assignment