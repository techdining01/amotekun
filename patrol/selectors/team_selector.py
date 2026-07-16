from ..models import PatrolTeam, PatrolMembership
from django.db.models import Prefetch

class TeamSelector:

    @staticmethod
    def all():

        return PatrolTeam.objects.select_related(
            "agency",
            "commander",
        )

    @staticmethod
    def active():

        return PatrolTeam.objects.filter(
            active=True,
        )

    @staticmethod
    def available():

        return PatrolTeam.objects.filter(
            status="AVAILABLE",
            active=True,
        )

    @staticmethod
    def by_id(team_id):

        return PatrolTeam.objects.select_related(
            "agency",
            "commander",
        ).get(
            pk=team_id,
        )

    @staticmethod
    def with_members():

        return PatrolTeam.objects.prefetch_related(

            Prefetch(

                "memberships",

                queryset=PatrolMembership.objects.select_related(
                    "personnel",
                    "personnel__user",
                ),

            )

        )
