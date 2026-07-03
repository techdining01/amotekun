from celery import shared_task
from traffic.services import TrafficCollectionService


@shared_task(bind=True)
def collect_traffic_snapshot(self, provider_name="tomtom"):
    """Collect traffic snapshots on a schedule."""
    service = TrafficCollectionService(provider_name=provider_name)
    snapshots = service.collect(dry_run=False)
    return {
        "provider": provider_name,
        "snapshots_collected": len(snapshots),
    }
