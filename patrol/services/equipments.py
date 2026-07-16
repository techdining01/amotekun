
from django.utils import timezone
from ..choices import EquipmentStatus
from ..models import EquipmentAssignment


class EquipmentService:

    @staticmethod
    def assign(
        equipment,
        personnel,
    ):

        return EquipmentAssignment.objects.create(

            equipment=equipment,

            personnel=personnel,

        )

    @staticmethod
    def return_equipment(assignment):

        assignment.active = False

        assignment.returned_at = timezone.now()

        assignment.save()

        equipment = assignment.equipment

        equipment.status = EquipmentStatus.AVAILABLE

        equipment.save()

        return assignment