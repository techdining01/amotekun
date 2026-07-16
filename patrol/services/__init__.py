from django.db import transaction
from django.utils import timezone

from ..models import (
    PatrolMission,
    PatrolTeam,
    Vehicle,
    VehicleAssignment,
    GPSPosition,
    PatrolCheckpoint,
    EquipmentAssignment,
)
from ..choices import (
    MissionStatus,
    PatrolTeamStatus,
    VehicleStatus,
    CheckpointStatus,
)