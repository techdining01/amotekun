from .models import TrafficSnapshot, TrafficIncident, TrafficCamera, TrafficFlow, Road
from .providers import get_traffic_provider
import logging


logger = logging.getLogger(__name__)


class TrafficCollectionService:
    def __init__(self, provider_name: str = "tomtom"):
        self.provider_name = provider_name.lower()
        self.provider = get_traffic_provider(self.provider_name)

    def collect(self, roads=None, dry_run: bool = False, logger=None):
        if roads is None:
            roads = Road.objects.filter(is_monitored=True)

        snapshots = []
        for road in roads:
            try:
                snapshot_payload = self.provider.fetch_snapshot(road)
            except Exception as exc:
                if logger:
                    logger.exception(
                        "Provider %s failed fetching data for road %s: %s",
                        self.provider_name,
                        road.name,
                        exc,
                    )
                continue

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
                road.last_flow_update = snapshot.timestamp
                road.save(update_fields=["last_flow_update"])

                if snapshot.average_speed is not None:
                    congestion_level = snapshot.congestion_level
                    if congestion_level not in {"free", "moderate", "heavy", "severe"}:
                        congestion_level = "free"
                    TrafficFlow.objects.create(
                        road=road,
                        vehicle_count=0,
                        average_speed=snapshot.average_speed,
                        congestion_level=congestion_level,
                    )
            snapshots.append(snapshot)

        return snapshots
