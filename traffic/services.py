from .models import TrafficSnapshot, TrafficIncident, TrafficCamera, Road
from .providers import HereTrafficProvider, TomTomTrafficProvider, MockTrafficProvider


PROVIDER_CLASSES = {
    "tomtom": TomTomTrafficProvider,
    "here": HereTrafficProvider,
    "mock": MockTrafficProvider,
}


def get_traffic_provider(provider_name: str):
    provider_class = PROVIDER_CLASSES.get(provider_name.lower())
    if not provider_class:
        raise ValueError(f"Unknown traffic provider: {provider_name}")
    return provider_class()


class TrafficCollectionService:
    def __init__(self, provider_name: str = "tomtom"):
        self.provider_name = provider_name.lower()
        self.provider = get_traffic_provider(self.provider_name)

    def collect(self, roads=None, dry_run: bool = False):
        if roads is None:
            roads = Road.objects.filter(is_monitored=True)

        snapshots = []
        for road in roads:
            try:
                snapshot_payload = self.provider.fetch_snapshot(road)
            except Exception as exc:
                if self.provider_name == "tomtom":
                    backup_provider = HereTrafficProvider()
                    snapshot_payload = backup_provider.fetch_snapshot(road)
                else:
                    snapshot_payload = MockTrafficProvider().fetch_snapshot(road)

            snapshot_payload["incident_count"] = TrafficIncident.objects.filter(
                road_name__iexact=road.name,
                status="active",
            ).count()
            snapshot_payload["camera_count"] = TrafficCamera.objects.filter(
                monitored_road=road
            ).count()
            snapshot = TrafficSnapshot(**snapshot_payload)
            if not dry_run:
                snapshot.save()
            snapshots.append(snapshot)

        return snapshots
