from celery import shared_task
import logging
from traffic.services import TrafficCollectionService


@shared_task(bind=True)
def collect_traffic_snapshot(self, provider_name="tomtom"):
    """Collect traffic snapshots on a schedule with explicit provider-fallback logging."""
    logger = logging.getLogger("traffic.tasks")

    # Try primary provider
    try:
        service = TrafficCollectionService(provider_name=provider_name)
        snapshots = service.collect(dry_run=False, logger=logger)
        logger.info(
            "Collected %d snapshots using provider %s", len(snapshots), provider_name
        )
        return {"provider": provider_name, "snapshots_collected": len(snapshots)}
    except Exception as exc:
        logger.exception(
            "Primary provider '%s' failed during collection: %s", provider_name, exc
        )

    # Fallback chain
    for fallback in ("here",):
        if fallback == provider_name:
            continue
        try:
            service = TrafficCollectionService(provider_name=fallback)
            snapshots = service.collect(dry_run=False, logger=logger)
            logger.info(
                "Fallback provider '%s' succeeded after '%s' failure; collected %d snapshots",
                fallback,
                provider_name,
                len(snapshots),
            )
            return {"provider": fallback, "snapshots_collected": len(snapshots)}
        except Exception as e:
            logger.exception("Fallback provider '%s' failed as well: %s", fallback, e)

    logger.error("All traffic providers failed for scheduled collection.")
    raise RuntimeError("All traffic providers failed during scheduled collection")
