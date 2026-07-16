from reports.models import (
    Incident,
    FloodZone,
)

from analytics.models import Hotspot

from surveillance.models import Camera

from patrol.models import PatrolTeam

from dispatch.models import Dispatch

from traffic.models import TrafficIncident, Road

from stations.models import AmotekunStation, PoliceStation, Hospital


class MapDataService:
    """
    Aggregates GIS data from all applications
    for dashboard map rendering.
    """

    @staticmethod
    def incidents():

        queryset = Incident.objects.select_related("reporter").all()

        return queryset

    @staticmethod
    def dispatches():

        return Dispatch.objects.select_related(
            "incident",
            "patrol_team",
        ).exclude(status="resolved")

    @staticmethod
    def patrol_units():

        return PatrolTeam.objects.select_related(
            "vehicle",
        ).all()

    @staticmethod
    def cameras():

        return Camera.objects.filter(status="online").select_related("location")

    @staticmethod
    def hotspots():

        return Hotspot.objects.order_by("-intensity_score")[:100]

    @staticmethod
    def crime_hotspots():

        return Hotspot.objects.all() if Hotspot.objects.exists() else None

    @staticmethod
    def flood_zones():

        return FloodZone.objects.all() if FloodZone.objects.exists() else None

    @staticmethod
    def roads():

        return Road.objects.all() if Road.objects.exists() else None

    @staticmethod
    def traffic():

        return (
            TrafficIncident.objects.all() if TrafficIncident.objects.exists() else None
        )

    @staticmethod
    def summary():

        return {
            "incidents": Incident.objects.count(),
            "active_dispatches": Dispatch.objects.exclude(status="resolved").count(),
            "active_hotspots": Hotspot.objects.count(),
            "active_cameras": Camera.objects.filter(status="online").count(),
            "active_patrols": PatrolTeam.objects.count(),
        }

    @staticmethod
    def state_data(state):

        return {
            "incidents": Incident.objects.filter(state=state),
            "dispatches": Dispatch.objects.filter(state=state),
            "hotspots": Hotspot.objects.filter(state=state)
            if hasattr(Hotspot, "state")
            else Hotspot.objects.none(),
        }

    @staticmethod
    def lga_data(lga):

        return {
            "incidents": Incident.objects.filter(lga=lga),
            "dispatches": Dispatch.objects.filter(lga=lga),
        }

    @staticmethod
    def ward_data(ward):

        return {
            "incidents": Incident.objects.none(),
            "dispatches": Dispatch.objects.none(),
        }

    @staticmethod
    def police_stations():
        return PoliceStation.objects.all()

    @staticmethod
    def amotekun_stations():
        return AmotekunStation.objects.all()

    @staticmethod
    def hospitals():
        return Hospital.objects.all()

    @staticmethod
    def public_layers():
        return {
            "incidents": MapDataService.incidents(),
            "hotspots": MapDataService.hotspots(),
            "police_stations": MapDataService.police_stations(),
            "hospitals": MapDataService.hospitals(),
        }

    @staticmethod
    def map_payload():
        return {
            # operations
            "incidents": MapDataService.incidents(),
            "dispatches": MapDataService.dispatches(),
            "patrols": MapDataService.patrol_units(),
            "hotspots": MapDataService.hotspots(),
            "flood_zones": MapDataService.flood_zones(),
            # infrastructure
            "roads": MapDataService.roads(),
            "cameras": MapDataService.cameras(),
            "police_stations": MapDataService.police_stations(),
            "amotekun_stations": MapDataService.amotekun_stations(),
            "hospitals": MapDataService.hospitals(),
            "states": MapDataService.state_data(state=None),
            "lgas": MapDataService.lga_data(lga=None),
            "wards": MapDataService.ward_data(ward=None),
            "traffic": MapDataService.traffic(),
        }


