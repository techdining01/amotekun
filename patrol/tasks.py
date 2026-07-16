from celery import shared_task


@shared_task
def cleanup_old_gps():
    from patrol.services.gps import GPSService
    GPSService.cleanup_old_positions()
    return "completed"


@shared_task
def patrol_heartbeat():
    from patrol.selectors.mission_selector import MissionSelector
    from patrol.services.mission import MissionService
    for mission in MissionSelector.active():
        MissionService.verify_status(mission)
    return "completed"


@shared_task
def detect_route_deviation():
    from patrol.selectors.mission_selector import MissionSelector
    from patrol.services.navigation import NavigationService
    for mission in MissionSelector.active():
        NavigationService.detect_deviation(mission)
    return "completed"


@shared_task
def geofence_monitor():
    from patrol.services.geofence import GeofenceService
    GeofenceService.monitor()
    return "completed"


@shared_task
def vehicle_health():
    from patrol.services.tracking import TrackingService
    TrackingService.check_vehicle_health()
    return "completed"


@shared_task
def gps_offline():
    from patrol.services.gps import GPSService
    GPSService.detect_offline_trackers()
    return "completed"


@shared_task
def patrol_idle():
    from patrol.services.tracking import TrackingService
    TrackingService.detect_idle_patrols()
    return "completed"


@shared_task
def shift_reminders():
    from patrol.services.patrol import PatrolService
    PatrolService.send_shift_reminders()
    return "completed"


@shared_task
def auto_close_shift():
    from patrol.selectors.shift_selector import ShiftSelector
    from django.utils import timezone
    ShiftSelector.active().filter(ends_at__lte=timezone.now()).update(active=False)
    return "completed"


@shared_task
def patrol_statistics():
    from patrol.services.patrol import PatrolService
    PatrolService.refresh_statistics()
    return "completed"


@shared_task
def refresh_dashboard():
    from patrol.services.patrol import PatrolService
    PatrolService.refresh_dashboard_cache()
    return "completed"


@shared_task
def generate_daily_report():
    from patrol.services.patrol import PatrolService
    PatrolService.daily_report()
    return "completed"


@shared_task
def weekly_report():
    from patrol.services.patrol import PatrolService
    PatrolService.weekly_summary()
    return "completed"


@shared_task
def ai_prediction():
    from patrol.services.patrol import PatrolService
    PatrolService.request_ai_prediction()
    return "completed"


@shared_task
def refresh_hotspots():
    from analytics.services.hotspot_service import HotspotService
    HotspotService().run_analysis()
    return "completed"


@shared_task
def correlate_camera():
    from patrol.services.patrol import PatrolService
    PatrolService.link_nearby_cameras()
    return "completed"


@shared_task
def update_traffic():
    from patrol.services.patrol import PatrolService
    PatrolService.update_traffic_conditions()
    return "completed"


@shared_task
def notify_chat():
    from patrol.services.patrol import PatrolService
    PatrolService.notify_chat_rooms()
    return "completed"


@shared_task
def panic_escalation():
    from patrol.services.patrol import PatrolService
    PatrolService.escalate_panic()
    return "completed"


@shared_task
def mission_timeout():
    from patrol.services.mission import MissionService
    from patrol.selectors.mission_selector import MissionSelector
    from django.utils import timezone
    from datetime import timedelta
    stale = MissionSelector.active().filter(
        started_at__lte=timezone.now() - timedelta(hours=12)
    )
    for mission in stale:
        MissionService.complete(mission, outcome="FAILED", notes="Auto-closed: timeout")
    return f"timed out {stale.count()} missions"
