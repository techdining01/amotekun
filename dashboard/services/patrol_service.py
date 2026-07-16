from django.utils import timezone
from django.db.models import Count, Avg

from patrol.models import (
    PatrolTeam,
    PatrolMission,
    Vehicle,
    GPSPosition,
    PatrolShift,
    PatrolEquipment,
)
from patrol.choices import PatrolTeamStatus, MissionStatus, VehicleStatus


class PatrolService:
    @staticmethod
    def summary():
        now = timezone.now()
        teams = PatrolTeam.objects.all()
        missions = PatrolMission.objects.all()

        return {
            "teams": {
                "total": teams.count(),
                "available": teams.filter(status=PatrolTeamStatus.AVAILABLE).count(),
                "on_patrol": teams.filter(status=PatrolTeamStatus.ON_PATROL).count(),
                "dispatched": teams.filter(status=PatrolTeamStatus.DISPATCHED).count(),
                "offline": teams.filter(status=PatrolTeamStatus.OFFLINE).count(),
            },
            "missions": {
                "total": missions.count(),
                "active": missions.filter(
                    status__in=[
                        MissionStatus.EN_ROUTE,
                        MissionStatus.ARRIVED,
                        MissionStatus.IN_PROGRESS,
                    ]
                ).count(),
                "pending": missions.filter(status=MissionStatus.PENDING).count(),
                "completed_today": missions.filter(
                    status=MissionStatus.COMPLETED,
                    completed_at__date=now.date(),
                ).count(),
            },
            "vehicles": {
                "total": Vehicle.objects.count(),
                "available": Vehicle.objects.filter(
                    status=VehicleStatus.AVAILABLE
                ).count(),
                "on_patrol": Vehicle.objects.filter(
                    status=VehicleStatus.ON_PATROL
                ).count(),
                "maintenance": Vehicle.objects.filter(
                    status=VehicleStatus.MAINTENANCE
                ).count(),
            },
        }

    @staticmethod
    def active_missions():
        return (
            PatrolMission.objects.filter(
                status__in=[
                    MissionStatus.EN_ROUTE,
                    MissionStatus.ARRIVED,
                    MissionStatus.IN_PROGRESS,
                ]
            )
            .select_related("patrol_team", "incident", "vehicle_assignment__vehicle")
            .order_by("-started_at")
        )

    @staticmethod
    def team_locations():
        latest_positions = (
            GPSPosition.objects.filter(
                mission__status__in=[
                    MissionStatus.EN_ROUTE,
                    MissionStatus.ARRIVED,
                    MissionStatus.IN_PROGRESS,
                ]
            )
            .select_related("mission__patrol_team", "vehicle")
            .order_by("mission", "-recorded_at")
            .distinct("mission")
        )
        return [
            {
                "team": pos.mission.patrol_team.name
                if pos.mission.patrol_team
                else None,
                "vehicle": str(pos.vehicle) if pos.vehicle else None,
                "lat": pos.location.y,
                "lng": pos.location.x,
                "speed": pos.speed,
                "heading": pos.heading,
                "recorded_at": pos.recorded_at,
            }
            for pos in latest_positions
        ]

    @staticmethod
    def active_shifts():
        now = timezone.now()
        return PatrolShift.objects.filter(
            active=True, starts_at__lte=now, ends_at__gte=now
        ).select_related("team")

    @staticmethod
    def mission_performance():
        return PatrolMission.objects.filter(status=MissionStatus.COMPLETED).aggregate(
            total_completed=Count("id"),
            avg_duration=Avg("completed_at") - Avg("started_at"),
        )
