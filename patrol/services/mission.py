from django.db import transaction
from django.utils import timezone

from ..models import PatrolMission
from ..choices import MissionStatus, PatrolTeamStatus, VehicleStatus


class MissionService:
    @staticmethod
    @transaction.atomic
    def create_from_dispatch(
        dispatch,
        incident,
        team,
        vehicle_assignment,
        priority,
    ):

        mission = PatrolMission.objects.create(
            dispatch=dispatch,
            incident=incident,
            patrol_team=team,
            vehicle_assignment=vehicle_assignment,
            priority=priority,
        )

        team.status = PatrolTeamStatus.DISPATCHED
        team.save(update_fields=["status"])

        vehicle = vehicle_assignment.vehicle
        vehicle.status = VehicleStatus.ASSIGNED
        vehicle.save(update_fields=["status"])

        return mission

    @staticmethod
    @transaction.atomic
    def start(mission):

        mission.status = MissionStatus.EN_ROUTE

        mission.started_at = timezone.now()

        mission.save(
            update_fields=[
                "status",
                "started_at",
            ]
        )

        team = mission.patrol_team

        if team:
            team.status = PatrolTeamStatus.ON_PATROL

            team.save(update_fields=["status"])

        vehicle_assignment = mission.vehicle_assignment

        if vehicle_assignment:
            vehicle = vehicle_assignment.vehicle

            vehicle.status = VehicleStatus.ON_PATROL

            vehicle.save(update_fields=["status"])

        return mission

    @staticmethod
    def arrive(mission):

        mission.status = MissionStatus.ARRIVED

        mission.save(
            update_fields=[
                "status",
            ]
        )

        return mission

    @staticmethod
    @transaction.atomic
    def complete(
        mission,
        outcome,
        notes="",
    ):

        mission.status = MissionStatus.COMPLETED

        mission.completed_at = timezone.now()

        mission.outcome = outcome

        mission.notes = notes

        mission.save()

        team = mission.patrol_team

        if team:
            team.status = PatrolTeamStatus.AVAILABLE

            team.save()

        assignment = mission.vehicle_assignment

        if assignment:
            assignment.active = False

            assignment.released_at = timezone.now()

            assignment.save()

            vehicle = assignment.vehicle

            vehicle.status = VehicleStatus.AVAILABLE

            vehicle.save()

        return mission
