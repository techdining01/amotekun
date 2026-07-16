from django.contrib.gis.geos import Point

from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .models import (
    PatrolMission,
    PatrolTeam,
    Vehicle,
    GPSPosition,
    PatrolEquipment,
    PatrolShift,
)

from .serializers import (
    PatrolMissionSerializer,
    PatrolTeamSerializer,
    VehicleSerializer,
    GPSSerializer,
    PatrolEquipmentSerializer,
    PatrolShiftSerializer,
)

from .selectors.mission_selector import MissionSelector
from .selectors.team_selector import TeamSelector
from .services.mission import MissionService
from .services.patrol import PatrolService
from .services.gps import GPSService


class VehicleViewSet(ModelViewSet):
    serializer_class = VehicleSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Vehicle.objects.all()

    @action(detail=False)
    def available(self, request):
        serializer = self.get_serializer(Vehicle.objects.available(), many=True)
        return Response(serializer.data)


class PatrolTeamViewSet(ModelViewSet):
    serializer_class = PatrolTeamSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = PatrolTeam.objects.all()

    @action(detail=False)
    def available(self, request):
        serializer = self.get_serializer(TeamSelector.available(), many=True)
        return Response(serializer.data)


class PatrolMissionViewSet(ModelViewSet):
    serializer_class = PatrolMissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = PatrolMission.objects.all()

    @action(detail=False)
    def active(self, request):
        serializer = self.get_serializer(MissionSelector.active(), many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def start(self, request, pk=None):
        mission = self.get_object()
        MissionService.start(mission)
        return Response(self.get_serializer(mission).data)

    @action(detail=True, methods=["post"])
    def arrive(self, request, pk=None):
        mission = self.get_object()
        MissionService.arrive(mission)
        return Response(self.get_serializer(mission).data)

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        mission = self.get_object()
        MissionService.complete(
            mission,
            outcome=request.data.get("outcome"),
            notes=request.data.get("notes"),
        )
        return Response(self.get_serializer(mission).data)

    @action(detail=False, methods=["post"])
    def dispatch(self, request):
        mission = PatrolService.dispatch(
            dispatch=request.data["dispatch"],
            incident=request.data["incident"],
            team=request.data["team"],
            vehicle=request.data["vehicle"],
            priority=request.data["priority"],
        )
        return Response(self.get_serializer(mission).data, status=status.HTTP_201_CREATED)


class GPSPositionViewSet(ModelViewSet):
    serializer_class = GPSSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = GPSPosition.objects.all()

    @action(detail=False, methods=["post"])
    def record(self, request):
        point = Point(
            float(request.data["longitude"]),
            float(request.data["latitude"]),
            srid=4326,
        )
        gps = GPSService.record(
            mission=request.data["mission"],
            vehicle=request.data["vehicle"],
            point=point,
            heading=request.data.get("heading"),
            speed=request.data.get("speed"),
            accuracy=request.data.get("accuracy"),
        )
        return Response(self.get_serializer(gps).data)


class PatrolEquipmentViewSet(ModelViewSet):
    serializer_class = PatrolEquipmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = PatrolEquipment.objects.all()


class PatrolShiftViewSet(ModelViewSet):
    serializer_class = PatrolShiftSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = PatrolShift.objects.all()


class PatrolDashboardAPIView(ReadOnlyModelViewSet):
    serializer_class = PatrolTeamSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = PatrolTeam.objects.none()

    @action(detail=False)
    def summary(self, request):
        from dashboard.services.patrol_service import PatrolService as DashPatrolService
        return Response(DashPatrolService.summary())


class PatrolMapAPIView(ReadOnlyModelViewSet):
    serializer_class = GPSSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = GPSPosition.objects.none()

    def list(self, request):
        from dashboard.services.patrol_service import PatrolService as DashPatrolService
        return Response(DashPatrolService.team_locations())


class ResponderAPIView(ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = PatrolMission.objects.none()
    serializer_class = PatrolMissionSerializer

    @action(detail=False)
    def my_mission(self, request):
        mission = PatrolMission.objects.filter(
            patrol_team__memberships__personnel__user=request.user,
            status__in=["EN_ROUTE", "ARRIVED", "IN_PROGRESS"],
        ).first()
        if not mission:
            return Response({"detail": "No active mission."}, status=status.HTTP_404_NOT_FOUND)
        return Response(self.get_serializer(mission).data)


class PatrolCommanderAPIView(ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = PatrolTeam.objects.none()
    serializer_class = PatrolTeamSerializer

    @action(detail=False)
    def team_status(self, request):
        teams = PatrolTeam.objects.filter(
            commander=request.user
        ).prefetch_related("memberships", "dispatches")
        return Response(PatrolTeamSerializer(teams, many=True).data)
