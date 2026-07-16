from ..models import PatrolMission

class MissionSelector:

    @staticmethod
    def active():

        return PatrolMission.objects.exclude(
            status="COMPLETED",
        ).exclude(
            status="CANCELLED",
        )

    @staticmethod
    def by_dispatch(dispatch):

        return PatrolMission.objects.filter(
            dispatch=dispatch,
        ).first()

    @staticmethod
    def current(team):

        return PatrolMission.objects.filter(

            patrol_team=team,

        ).exclude(

            status="COMPLETED",

        ).first()

    @staticmethod
    def today():

        from django.utils import timezone

        today = timezone.now().date()

        return PatrolMission.objects.filter(

            started_at__date=today,

        )

    @staticmethod
    def completed():

        return PatrolMission.objects.filter(
            status="COMPLETED",
        )
