from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Camera, CameraRecording, CameraAlert
from .serializers import CameraSerializer, CameraRecordingSerializer, CameraAlertSerializer


class CameraViewSet(viewsets.ModelViewSet):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Camera.objects.all()
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset
    
    @action(detail=True, methods=['post'])
    def mark_online(self, request, pk=None):
        """Mark camera as online"""
        camera = self.get_object()
        camera.mark_online()
        return Response({'status': 'online'})
    
    @action(detail=True, methods=['post'])
    def mark_offline(self, request, pk=None):
        """Mark camera as offline"""
        camera = self.get_object()
        camera.mark_offline()
        return Response({'status': 'offline'})


class CameraRecordingViewSet(viewsets.ModelViewSet):
    queryset = CameraRecording.objects.all()
    serializer_class = CameraRecordingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = CameraRecording.objects.all()
        camera_id = self.request.query_params.get('camera')
        if camera_id:
            queryset = queryset.filter(camera_id=camera_id)
        return queryset


class CameraAlertViewSet(viewsets.ModelViewSet):
    queryset = CameraAlert.objects.all()
    serializer_class = CameraAlertSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = CameraAlert.objects.all()
        camera_id = self.request.query_params.get('camera')
        if camera_id:
            queryset = queryset.filter(camera_id=camera_id)
        
        acknowledged = self.request.query_params.get('acknowledged')
        if acknowledged:
            queryset = queryset.filter(acknowledged=acknowledged.lower() == 'true')
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def acknowledge(self, request, pk=None):
        """Acknowledge an alert"""
        alert = self.get_object()
        alert.acknowledge(request.user)
        return Response({'status': 'acknowledged'})
    
    @action(detail=False, methods=['get'])
    def unacknowledged(self, request):
        """Get all unacknowledged alerts"""
        alerts = CameraAlert.objects.filter(acknowledged=False)
        serializer = self.get_serializer(alerts, many=True)
        return Response(serializer.data)
