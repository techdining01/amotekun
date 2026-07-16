
from ..models import PatrolShift

class ShiftSelector:

    @staticmethod
    def active():

        return PatrolShift.objects.filter(
            active=True,
        )

    @staticmethod
    def team(team):

        return PatrolShift.objects.filter(
            team=team,
            active=True,
        ).first()