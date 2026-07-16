
from ..models import VehicleAssignment

class AssignmentSelector:

    @staticmethod
    def active():

        return VehicleAssignment.objects.filter(
            active=True,
        )

    @staticmethod
    def team(team):

        return VehicleAssignment.objects.filter(
            patrol_team=team,
            active=True,
        ).first()

