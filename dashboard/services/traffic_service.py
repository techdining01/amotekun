from stations.models import PoliceStation, AmotekunStation, Hospital
from patrol.models import PatrolTeam


class RoutingService:

    @staticmethod
    def nearest_police_station(point):
        return PoliceStation.objects.distance(point).order_by("distance").first()
    
    @staticmethod
    def nearest_amotekun_station(point):
        return (
            AmotekunStation.objects
            .distance(point)
            .order_by("distance")
            .first()
        )
    
    @staticmethod
    def nearest_hospital(point):
        return (
            Hospital.objects
            .distance(point)
            .order_by("distance")
            .first()
        )

    @staticmethod
    def nearest_patrol_team(point):
        return (
            PatrolTeam.objects
            .filter(
                status="AVAILABLE"
            )
            .distance(point)
            .order_by("distance")
            .first()
        )

    @staticmethod
    def fastest_route(origin, destination):
        return {
            "origin": origin,
            "destination": destination,
            "route": [],
            "estimated_time": 0,
            "distance": 0,
        }
