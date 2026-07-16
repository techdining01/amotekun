
from ..models import EquipmentAssignment

class EquipmentSelector:

    @staticmethod
    def assigned():

        return EquipmentAssignment.objects.filter(
            active=True,
        )

    @staticmethod
    def personnel(personnel):

        return EquipmentAssignment.objects.filter(

            personnel=personnel,

            active=True,

        )
