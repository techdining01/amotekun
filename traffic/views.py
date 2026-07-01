from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.utils import timezone
from .models import TrafficIncident, TrafficFlow, Road, TrafficCamera, TrafficAlert
from .serializers import (
    TrafficIncidentSerializer, TrafficFlowSerializer, 
    RoadSerializer, TrafficCameraSerializer, TrafficAlertSerializer
)


class TrafficIncidentViewSet(viewsets.ModelViewSet):
    queryset = TrafficIncident.objects.all()
    serializer_class = TrafficIncidentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = TrafficIncident.objects.all()
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by severity
        severity = self.request.query_params.get('severity')
        if severity:
            queryset = queryset.filter(severity=severity)
        
        # Filter by incident type
        incident_type = self.request.query_params.get('incident_type')
        if incident_type:
            queryset = queryset.filter(incident_type=incident_type)
        
        # Spatial filter - incidents within radius
        lat = self.request.query_params.get('lat')
        lng = self.request.query_params.get('lng')
        radius = self.request.query_params.get('radius')
        if lat and lng and radius:
            point = Point(float(lng), float(lat), srid=4326)
            queryset = queryset.filter(location__distance_lte=(point, D(km=float(radius))))
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        """Resolve a traffic incident"""
        incident = self.get_object()
        incident.status = 'resolved'
        incident.resolved_by = request.user
        incident.resolved_at = timezone.now()
        incident.save()
        return Response({'status': 'resolved'})
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get all active traffic incidents"""
        incidents = self.queryset.filter(status='active')
        serializer = self.get_serializer(incidents, many=True)
        return Response(serializer.data)


class TrafficFlowViewSet(viewsets.ModelViewSet):
    queryset = TrafficFlow.objects.all()
    serializer_class = TrafficFlowSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = TrafficFlow.objects.all()
        
        # Filter by road
        road_id = self.request.query_params.get('road')
        if road_id:
            queryset = queryset.filter(road_id=road_id)
        
        # Filter by congestion level
        congestion = self.request.query_params.get('congestion_level')
        if congestion:
            queryset = queryset.filter(congestion_level=congestion)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def latest(self, request):
        """Get latest traffic flow measurements"""
        flows = self.queryset.order_by('-measured_at')[:100]
        serializer = self.get_serializer(flows, many=True)
        return Response(serializer.data)


class RoadViewSet(viewsets.ModelViewSet):
    queryset = Road.objects.all()
    serializer_class = RoadSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = Road.objects.all()
        
        # Filter by road type
        road_type = self.request.query_params.get('road_type')
        if road_type:
            queryset = queryset.filter(road_type=road_type)
        
        # Filter by monitored status
        is_monitored = self.request.query_params.get('is_monitored')
        if is_monitored:
            queryset = queryset.filter(is_monitored=is_monitored.lower() == 'true')
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def monitored(self, request):
        """Get all monitored roads"""
        roads = self.queryset.filter(is_monitored=True)
        serializer = self.get_serializer(roads, many=True)
        return Response(serializer.data)


class TrafficCameraViewSet(viewsets.ModelViewSet):
    queryset = TrafficCamera.objects.all()
    serializer_class = TrafficCameraSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    @action(detail=True, methods=['post'])
    def reset_count(self, request, pk=None):
        """Reset daily vehicle count"""
        camera = self.get_object()
        camera.daily_vehicle_count = 0
        camera.save()
        return Response({'status': 'count reset'})


class TrafficAlertViewSet(viewsets.ModelViewSet):
    queryset = TrafficAlert.objects.all()
    serializer_class = TrafficAlertSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = TrafficAlert.objects.all()
        
        # Filter by alert type
        alert_type = self.request.query_params.get('alert_type')
        if alert_type:
            queryset = queryset.filter(alert_type=alert_type)
        
        # Filter by severity
        severity = self.request.query_params.get('severity')
        if severity:
            queryset = queryset.filter(severity=severity)
        
        # Filter by acknowledgment status
        acknowledged = self.request.query_params.get('acknowledged')
        if acknowledged:
            queryset = queryset.filter(acknowledged=acknowledged.lower() == 'true')
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def acknowledge(self, request, pk=None):
        """Acknowledge a traffic alert"""
        alert = self.get_object()
        alert.acknowledged = True
        alert.acknowledged_by = request.user
        alert.acknowledged_at = timezone.now()
        alert.save()
        return Response({'status': 'acknowledged'})
    
    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        """Resolve a traffic alert"""
        alert = self.get_object()
        alert.resolved_at = timezone.now()
        alert.save()
        return Response({'status': 'resolved'})
    
    @action(detail=False, methods=['get'])
    def unacknowledged(self, request):
        """Get all unacknowledged alerts"""
        alerts = self.queryset.filter(acknowledged=False)
        serializer = self.get_serializer(alerts, many=True)
        return Response(serializer.data)
