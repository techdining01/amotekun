import logging
from celery import shared_task
from decouple import config
from .models import Camera

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def camera_health_check(self):
    camera_id = config("CAMERA_DEVICE_ID", default=None)
    if not camera_id:
        logger.error("CAMERA_DEVICE_ID is not configured")
        return {"status": "error", "message": "CAMERA_DEVICE_ID not set"}

    try:
        camera = Camera.objects.get(camera_id=camera_id)
    except Camera.DoesNotExist:
        logger.error("Camera with id %s does not exist", camera_id)
        return {"status": "error", "message": "Camera not registered"}

    # Mark online when a registered camera has a stream URL configured.
    if camera.get_stream_url():
        camera.mark_online()
        logger.info("Camera %s marked online", camera_id)
        return {"status": "online", "camera_id": camera_id}

    camera.mark_offline()
    logger.warning("Camera %s has no stream URL configured", camera_id)
    return {"status": "offline", "camera_id": camera_id}
