
from django.conf import settings
from django.contrib.gis.db import models 

from accounts.models import Agency, PersonnelAssignment
from dispatch.models import Dispatch
from reports.models import Incident

from .choices import VehicleTypeCategory, PatrolTeamType, PatrolTeamStatus, VehicleStatus, FuelType, PatrolPriority, MissionStatus, MissionOutcome, CheckpointStatus, ShiftType, EquipmentType, EquipmentStatus, MaintenanceStatus


class VehicleType(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True,
    )

    category = models.CharField(
        max_length=30,
        choices=VehicleTypeCategory.choices,
    )

    description = models.TextField(
        blank=True,
    )

    def __str__(self):
        return self.name

class Vehicle(models.Model):

    agency = models.ForeignKey(
        Agency,
        on_delete=models.CASCADE,
        related_name="vehicles",
    )

    vehicle_type = models.ForeignKey(
        VehicleType,
        on_delete=models.PROTECT,
    )

    registration_number = models.CharField(
        max_length=50,
        unique=True,
    )

    make = models.CharField(
        max_length=100,
    )

    model = models.CharField(
        max_length=100,
    )

    color = models.CharField(
        max_length=50,
        blank=True,
    )

    year = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    fuel_type = models.CharField(
        max_length=20,
        choices=FuelType.choices,
    )

    status = models.CharField(
        max_length=30,
        choices=VehicleStatus.choices,
        default=VehicleStatus.AVAILABLE,
    )

    tracker_id = models.CharField(
        max_length=100,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        ordering = [
            "registration_number",
        ]

    def __str__(self):

        return self.registration_number


class PatrolTeam(models.Model):

    agency = models.ForeignKey(
        Agency,
        on_delete=models.CASCADE,
        related_name="patrol_teams",
    )

    commander = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="commanded_teams",
    )

    name = models.CharField(
        max_length=100,
    )

    team_type = models.CharField(
        max_length=40,
        choices=PatrolTeamType.choices,
    )

    status = models.CharField(
        max_length=30,
        choices=PatrolTeamStatus.choices,
        default=PatrolTeamStatus.AVAILABLE,
    )

    active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        ordering = [
            "name",
        ]

    def __str__(self):

        return self.name


class PatrolMembership(models.Model):

    team = models.ForeignKey(
        PatrolTeam,
        on_delete=models.CASCADE,
        related_name="memberships",
    )

    personnel = models.ForeignKey(
        PersonnelAssignment,
        on_delete=models.CASCADE,
    )

    joined_at = models.DateTimeField(
        auto_now_add=True,
    )

    is_team_lead = models.BooleanField(
        default=False,
    )

    class Meta:

        unique_together = [
            (
                "team",
                "personnel",
            )
        ]


class VehicleAssignment(models.Model):

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
    )

    patrol_team = models.ForeignKey(
        PatrolTeam,
        on_delete=models.CASCADE,
    )

    assigned_at = models.DateTimeField(
        auto_now_add=True,
    )

    released_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    active = models.BooleanField(
        default=True,
    )

class PatrolMission(models.Model):

    dispatch = models.OneToOneField(
        Dispatch,
        on_delete=models.CASCADE,
        related_name="patrol_mission",
    )

    incident = models.ForeignKey(
        Incident,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    patrol_team = models.ForeignKey(
        PatrolTeam,
        on_delete=models.SET_NULL,
        null=True,
    )

    vehicle_assignment = models.ForeignKey(
        VehicleAssignment,
        on_delete=models.SET_NULL,
        null=True,
    )

    priority = models.CharField(
        max_length=20,
        choices=PatrolPriority.choices,
        default=PatrolPriority.NORMAL,
    )

    status = models.CharField(
        max_length=30,
        choices=MissionStatus.choices,
        default=MissionStatus.PENDING,
    )

    started_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    outcome = models.CharField(
        max_length=30,
        choices=MissionOutcome.choices,
        blank=True,
    )

    notes = models.TextField(
        blank=True,
    )

    class Meta:

        ordering = [
            "-started_at",
        ]


class PatrolCheckpoint(models.Model):

    mission = models.ForeignKey(
        PatrolMission,
        on_delete=models.CASCADE,
        related_name="checkpoints",
    )

    name = models.CharField(
        max_length=150,
    )

    location = models.PointField(
        srid=4326,
    )

    status = models.CharField(
        max_length=20,
        choices=CheckpointStatus.choices,
        default=CheckpointStatus.PENDING,
    )

    arrived_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    departed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

class GPSPosition(models.Model):

    mission = models.ForeignKey(
        PatrolMission,
        on_delete=models.CASCADE,
        related_name="gps_points",
    )

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.SET_NULL,
        null=True,
    )

    location = models.PointField(
        srid=4326,
    )

    heading = models.FloatField(
        default=0,
    )

    speed = models.FloatField(
        default=0,
    )

    accuracy = models.FloatField(
        default=0,
    )

    recorded_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        ordering = [
            "-recorded_at",
        ]


class PatrolShift(models.Model):

    team = models.ForeignKey(
        PatrolTeam,
        on_delete=models.CASCADE,
    )

    shift_type = models.CharField(
        max_length=30,
        choices=ShiftType.choices,
    )

    starts_at = models.DateTimeField()

    ends_at = models.DateTimeField()

    active = models.BooleanField(
        default=True,
    )


class PatrolEquipment(models.Model):

    agency = models.ForeignKey(
        Agency,
        on_delete=models.CASCADE,
    )

    name = models.CharField(
        max_length=150,
    )

    equipment_type = models.CharField(
        max_length=50,
        choices=EquipmentType.choices,
    )

    serial_number = models.CharField(
        max_length=120,
        unique=True,
    )

    status = models.CharField(
        max_length=30,
        choices=EquipmentStatus.choices,
        default=EquipmentStatus.AVAILABLE,
    )


class EquipmentAssignment(models.Model):

    equipment = models.ForeignKey(
        PatrolEquipment,
        on_delete=models.CASCADE,
    )

    personnel = models.ForeignKey(
        PersonnelAssignment,
        on_delete=models.CASCADE,
    )

    assigned_at = models.DateTimeField(
        auto_now_add=True,
    )

    returned_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    active = models.BooleanField(
        default=True,
    )


class VehicleMaintenance(models.Model):

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
    )

    status = models.CharField(
        max_length=30,
        choices=MaintenanceStatus.choices,
    )

    description = models.TextField()

    scheduled_date = models.DateField()

    completed_date = models.DateField(
        null=True,
        blank=True,
    )


class VehicleFuelLog(models.Model):

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
    )

    litres = models.DecimalField(
        max_digits=8,
        decimal_places=2,
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    odometer = models.PositiveIntegerField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )


