from django.core.management.base import BaseCommand
from surveillance.models import Camera
from django.conf import settings
from decouple import config


class Command(BaseCommand):
    help = "Register a surveillance camera using environment camera_id and optional stream URL."

    def add_arguments(self, parser):
        parser.add_argument(
            "--name", type=str, help="Camera display name", default="V380 Camera"
        )
        parser.add_argument(
            "--description",
            type=str,
            help="Camera description",
            default="V380 wireless PTZ camera",
        )
        parser.add_argument("--hls_url", type=str, help="Optional HLS stream URL")
        parser.add_argument("--rtsp_url", type=str, help="Optional RTSP stream URL")
        parser.add_argument(
            "--camera_type",
            type=str,
            choices=[
                ("fixed", "Fixed"),
                ("ptz", "PTZ (Pan-Tilt-Zoom)"),
                ("dome", "Dome"),
                ("bullet", "Bullet"),
                ("thermal", "Thermal"),
            ],
            default="ptz",
        )
        parser.add_argument(
            "--ip_address", type=str, help="Optional IP address of the camera"
        )
        parser.add_argument(
            "--port", type=int, help="Optional port of the camera", default=80
        )
        parser.add_argument("--username", type=str, help="Optional camera username")
        parser.add_argument("--password", type=str, help="Optional camera password")

    def handle(self, *args, **options):
        camera_id = config("CAMERA_DEVICE_ID", default=None)
        if not camera_id:
            self.stderr.write(
                self.style.ERROR("CAMERA_DEVICE_ID not set in environment")
            )
            return

        camera, created = Camera.objects.get_or_create(
            camera_id=camera_id,
            defaults={
                "name": options["name"],
                "description": options["description"],
                "camera_type": options["camera_type"],
                "ip_address": options["ip_address"] or "",
                "port": options["port"],
                "rtsp_url": options["rtsp_url"] or "",
                "hls_url": options["hls_url"] or "",
                "status": "offline",
            },
        )

        if options["username"]:
            camera.username = options["username"]
        if options["password"]:
            camera.set_password(options["password"])
        if options["ip_address"]:
            camera.ip_address = options["ip_address"]
        if options["rtsp_url"]:
            camera.rtsp_url = options["rtsp_url"]
        if options["hls_url"]:
            camera.hls_url = options["hls_url"]

        camera.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f"Registered camera {camera_id}"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Updated camera {camera_id}"))
