from decouple import config
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Camera, CameraRecording, CameraAlert
from .serializers import (
    CameraSerializer,
    CameraRecordingSerializer,
    CameraAlertSerializer,
)


@login_required
def camera_grid_view(request):
    cameras = Camera.objects.all().order_by('name')
    return render(request, 'surveillance/camera_grid.html', {'cameras': cameras})


class CameraPagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = "page_size"
    max_page_size = 24


class CameraViewSet(viewsets.ModelViewSet):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CameraPagination

    def get_queryset(self):
        queryset = Camera.objects.all()
        status_filter = self.request.query_params.get("status")
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset

    @action(detail=False, methods=["post"], url_path="register-current")
    def register_current_device(self, request):
        camera_id = config("CAMERA_DEVICE_ID", default=None)
        if not camera_id:
            return Response(
                {"detail": "CAMERA_DEVICE_ID not configured."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = {
            "name": request.data.get("name", "V380 Camera"),
            "description": request.data.get("description", "V380 wireless PTZ camera"),
            "camera_type": request.data.get("camera_type", "ptz"),
            "ip_address": request.data.get("ip_address", ""),
            "port": request.data.get("port", 80),
            "rtsp_url": request.data.get("rtsp_url", ""),
            "hls_url": request.data.get("hls_url", ""),
            "control_url": request.data.get("control_url", ""),
            "status": "offline",
        }

        camera, created = Camera.objects.update_or_create(
            camera_id=camera_id,
            defaults=data,
        )

        username = request.data.get("username")
        password = request.data.get("password")
        if username:
            camera.username = username
        if password:
            camera.set_password(password)

        if camera.get_stream_url():
            camera.mark_online()
        else:
            camera.mark_offline()

        camera.save()
        serializer = self.get_serializer(camera)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"])
    def ptz(self, request, pk=None):
        camera = self.get_object()
        action_cmd = request.data.get("action")
        if not action_cmd:
            return Response(
                {"detail": "PTZ action is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        speed = request.data.get("speed", 1)
        preset = request.data.get("preset")

        try:
            result = camera.send_ptz_command(action_cmd, speed=speed, preset=preset)
            return Response(result)
        except Exception as exc:
            return Response(
                {"detail": str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=["post"])
    def mark_online(self, request, pk=None):
        """Mark camera as online"""
        camera = self.get_object()
        camera.mark_online()
        return Response({"status": "online"})

    @action(detail=True, methods=["post"])
    def mark_offline(self, request, pk=None):
        """Mark camera as offline"""
        camera = self.get_object()
        camera.mark_offline()
        return Response({"status": "offline"})


class CameraRecordingViewSet(viewsets.ModelViewSet):
    queryset = CameraRecording.objects.all()
    serializer_class = CameraRecordingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = CameraRecording.objects.all()
        camera_id = self.request.query_params.get("camera")
        if camera_id:
            queryset = queryset.filter(camera_id=camera_id)
        return queryset


class CameraAlertViewSet(viewsets.ModelViewSet):
    queryset = CameraAlert.objects.all()
    serializer_class = CameraAlertSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = CameraAlert.objects.all()
        camera_id = self.request.query_params.get("camera")
        if camera_id:
            queryset = queryset.filter(camera_id=camera_id)

        acknowledged = self.request.query_params.get("acknowledged")
        if acknowledged:
            queryset = queryset.filter(acknowledged=acknowledged.lower() == "true")

        return queryset

    @action(detail=True, methods=["post"])
    def acknowledge(self, request, pk=None):
        """Acknowledge an alert"""
        alert = self.get_object()
        alert.acknowledge(request.user)
        return Response({"status": "acknowledged"})

    @action(detail=False, methods=["get"])
    def unacknowledged(self, request):
        """Get all unacknowledged alerts"""
        alerts = CameraAlert.objects.filter(acknowledged=False)
        serializer = self.get_serializer(alerts, many=True)
        return Response(serializer.data)
