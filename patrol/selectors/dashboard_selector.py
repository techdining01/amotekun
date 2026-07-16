
from ..models import PatrolTeam, PatrolMission, Vehicle

class PatrolDashboardSelector:

    @staticmethod
    def summary():

        return {

            "teams": PatrolTeam.objects.count(),

            "available_teams":

                PatrolTeam.objects.filter(

                    status="AVAILABLE"

                ).count(),

            "active_missions":

                PatrolMission.objects.exclude(

                    status="COMPLETED",

                ).count(),

            "available_vehicles":

                Vehicle.objects.filter(

                    status="AVAILABLE",

                ).count(),

            "vehicles_on_patrol":

                Vehicle.objects.filter(

                    status="ON_PATROL",

                ).count(),

        }
