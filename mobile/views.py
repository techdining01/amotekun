from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.auth import get_user_model
from .models import MobileDevice, PushNotification
from .serializers import (
    MobileDeviceSerializer, PushNotificationSerializer, 
    DeviceRegistrationSerializer, MobileIncidentSerializer,
    FacilitySerializer, AmotekunFacilitySerializer, HospitalSerializer,
    MediaUploadSerializer
)
from reports.models import Incident, IncidentMedia
from stations.models import PoliceStation, AmotekunStation, Hospital
from dispatch.models import Dispatch
from dispatch.serializers import DispatchSerializer

User = get_user_model()


class MobileTokenObtainPairView(TokenObtainPairView):
    """Custom JWT token view for mobile"""
    permission_classes = (permissions.AllowAny,)


class MobileDeviceViewSet(viewsets.ModelViewSet):
    queryset = MobileDevice.objects.all()
    serializer_class = MobileDeviceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return MobileDevice.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # Check if device already exists for this user
        device_id = self.request.data.get('device_id')
        existing = MobileDevice.objects.filter(
            user=self.request.user,
            device_id=device_id
        ).first()
        
        if existing:
            # Update existing device

            serializer = self.get_serializer(existing, data=self.request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            self.object = existing
        else:
            # Create new device
            serializer.save(user=self.request.user)
            self.object = serializer.instance
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        """Register a mobile device for push notifications"""
        serializer = DeviceRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        device_id = serializer.validated_data['device_id']
        fcm_token = serializer.validated_data['fcm_token']
        
        # Check if device already exists
        existing = MobileDevice.objects.filter(
            user=request.user,
            device_id=device_id
        ).first()
        
        if existing:
            # Update existing device
            existing.fcm_token = fcm_token
            existing.is_active = True
            for field in ['device_type', 'app_version', 'os_version', 'device_name']:
                if field in serializer.validated_data:
                    setattr(existing, field, serializer.validated_data[field])
            existing.save()
            return Response(MobileDeviceSerializer(existing).data)
        else:
            # Create new device
            device = MobileDevice.objects.create(
                user=request.user,
                **serializer.validated_data
            )
            return Response(MobileDeviceSerializer(device).data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'])
    def unregister(self, request):
        """Unregister a mobile device"""
        device_id = request.data.get('device_id')
        if not device_id:
            return Response({'error': 'device_id required'}, status=status.HTTP_400_BAD_REQUEST)
        
        device = MobileDevice.objects.filter(
            user=request.user,
            device_id=device_id
        ).first()
        
        if device:
            device.is_active = False
            device.save()
            return Response({'status': 'unregistered'})
        
        return Response({'error': 'Device not found'}, status=status.HTTP_404_NOT_FOUND)


class PushNotificationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PushNotification.objects.all()
    serializer_class = PushNotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return PushNotification.objects.filter(recipient=self.request.user)


class MobileIncidentViewSet(viewsets.ModelViewSet):
    queryset = Incident.objects.all()
    serializer_class = MobileIncidentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Incident.objects.filter(reporter=self.request.user)

    def perform_create(self, serializer):
        lat = self.request.data.get('lat')
        lng = self.request.data.get('lng')
        if lat and lng:
            point = Point(float(lng), float(lat), srid=4326)
            try:
                from reports.views import get_location_from_point as get_loc
                state_name, lga_name = get_loc(point)
                serializer.save(reporter=self.request.user, geometry=point, state=state_name or 'Unknown', lga=lga_name or 'Unknown')
            except Exception:
                serializer.save(reporter=self.request.user, geometry=point)
        else:
            serializer.save(reporter=self.request.user)

    @action(detail=False, methods=['get'])
    def nearby(self, request):
        """Get incidents near a location (for officers)"""
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')
        radius = request.query_params.get('radius', 5)

        if lat and lng:
            point = Point(float(lng), float(lat), srid=4326)
            incidents = Incident.objects.filter(
                geometry__distance_lte=(point, D(km=float(radius)))
            )
            serializer = self.get_serializer(incidents, many=True)
            return Response(serializer.data)
        return Response({'error': 'lat and lng required'}, status=status.HTTP_400_BAD_REQUEST)


class FacilityViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def list(self, request):
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')
        facility_type = request.query_params.get('type')
        radius = request.query_params.get('radius', 10)

        if not lat or not lng:
            return Response({'error': 'lat and lng required'}, status=status.HTTP_400_BAD_REQUEST)

        point = Point(float(lng), float(lat), srid=4326)
        results = []

        if facility_type is None or facility_type in ['police', 'all']:
            police = PoliceStation.objects.filter(
                location__distance_lte=(point, D(km=float(radius)))
            )[:10]
            results.extend([{'type': 'police_station', 'data': FacilitySerializer(p).data} for p in police])

        if facility_type is None or facility_type in ['amotekun', 'all']:
            amotekun = AmotekunStation.objects.filter(
                location__distance_lte=(point, D(km=float(radius)))
            )[:10]
            results.extend([{'type': 'amotekun_station', 'data': AmotekunFacilitySerializer(a).data} for a in amotekun])

        if facility_type is None or facility_type in ['hospital', 'all']:
            hospitals = Hospital.objects.filter(
                location__distance_lte=(point, D(km=float(radius)))
            )[:10]
            results.extend([{'type': 'hospital', 'data': HospitalSerializer(h).data} for h in hospitals])

        return Response(results)


class MediaUploadViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        incident_id = request.data.get('incident')
        image = request.FILES.get('image')
        video = request.FILES.get('video')
        caption = request.data.get('caption', '')

        if not incident_id:
            return Response({'error': 'incident required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            incident = Incident.objects.get(pk=incident_id)
        except Incident.DoesNotExist:
            return Response({'error': 'Incident not found'}, status=status.HTTP_404_NOT_FOUND)

        if image:
            media = IncidentMedia.objects.create(
                incident=incident,
                media_type='image',
                file=image,
                caption=caption
            )
        elif video:
            media = IncidentMedia.objects.create(
                incident=incident,
                media_type='video',
                file=video,
                caption=caption
            )
        else:
            return Response({'error': 'image or video file required'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'status': 'uploaded', 'id': media.id}, status=status.HTTP_201_CREATED)


class MediaListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, incident_id):
        try:
            incident = Incident.objects.get(pk=incident_id)
            media = incident.media.all()
            return Response([{
                'id': m.id,
                'media_type': m.media_type,
                'file': m.file.url if m.file else None,
                'caption': m.caption,
                'uploaded_at': m.uploaded_at
            } for m in media])
        except Incident.DoesNotExist:
            return Response({'error': 'Incident not found'}, status=status.HTTP_404_NOT_FOUND)


class MobileDispatchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Dispatch.objects.all()
    serializer_class = DispatchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Dispatch.objects.filter(assigned_officer=self.request.user)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        dispatch = self.get_object()
        if dispatch.assigned_officer != request.user:
            return Response({'error': 'Not assigned to you'}, status=status.HTTP_403_FORBIDDEN)
        dispatch.transition_to('in_progress')
        return Response({'status': 'accepted'})

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        dispatch = self.get_object()
        if dispatch.assigned_officer != request.user:
            return Response({'error': 'Not assigned to you'}, status=status.HTTP_403_FORBIDDEN)
        dispatch.transition_to('resolved')
        return Response({'status': 'completed'})
