from django.db import models

class PatrolTeamType(models.TextChoices):

    RAPID_RESPONSE = (
        "RAPID_RESPONSE",
        "Rapid Response",
    )

    HIGHWAY_PATROL = (
        "HIGHWAY_PATROL",
        "Highway Patrol",
    )

    TRAFFIC_CONTROL = (
        "TRAFFIC_CONTROL",
        "Traffic Control",
    )

    INVESTIGATION = (
        "INVESTIGATION",
        "Investigation",
    )

    SWAT = (
        "SWAT",
        "SWAT",
    )

    MARINE = (
        "MARINE",
        "Marine Patrol",
    )

    DRONE = (
        "DRONE",
        "Drone Unit",
    )

    FIRE = (
        "FIRE",
        "Fire Response",
    )

    MEDICAL = (
        "MEDICAL",
        "Medical Response",
    )

    K9 = (
        "K9",
        "K9 Unit",
    )


class PatrolTeamStatus(models.TextChoices):

    AVAILABLE = (
        "AVAILABLE",
        "Available",
    )

    DISPATCHED = (
        "DISPATCHED",
        "Dispatched",
    )

    ON_PATROL = (
        "ON_PATROL",
        "On Patrol",
    )

    OFFLINE = (
        "OFFLINE",
        "Offline",
    )

    MAINTENANCE = (
        "MAINTENANCE",
        "Maintenance",
    )

class PatrolPriority(models.TextChoices):

    LOW = (
        "LOW",
        "Low",
    )

    NORMAL = (
        "NORMAL",
        "Normal",
    )

    HIGH = (
        "HIGH",
        "High",
    )

    CRITICAL = (
        "CRITICAL",
        "Critical",
    )

    EMERGENCY = (
        "EMERGENCY",
        "Emergency",
    )


class MissionStatus(models.TextChoices):

    PENDING = (
        "PENDING",
        "Pending",
    )

    ASSIGNED = (
        "ASSIGNED",
        "Assigned",
    )

    EN_ROUTE = (
        "EN_ROUTE",
        "En Route",
    )

    ARRIVED = (
        "ARRIVED",
        "Arrived",
    )

    IN_PROGRESS = (
        "IN_PROGRESS",
        "In Progress",
    )

    COMPLETED = (
        "COMPLETED",
        "Completed",
    )

    CANCELLED = (
        "CANCELLED",
        "Cancelled",
    )

    FAILED = (
        "FAILED",
        "Failed",
    )


class VehicleStatus(models.TextChoices):

    AVAILABLE = (
        "AVAILABLE",
        "Available",
    )

    ASSIGNED = (
        "ASSIGNED",
        "Assigned",
    )

    ON_PATROL = (
        "ON_PATROL",
        "On Patrol",
    )

    MAINTENANCE = (
        "MAINTENANCE",
        "Maintenance",
    )

    OUT_OF_SERVICE = (
        "OUT_OF_SERVICE",
        "Out Of Service",
    )


class VehicleTypeCategory(models.TextChoices):

    CAR = (
        "CAR",
        "Car",
    )

    PICKUP = (
        "PICKUP",
        "Pickup",
    )

    SUV = (
        "SUV",
        "SUV",
    )

    MOTORCYCLE = (
        "MOTORCYCLE",
        "Motorcycle",
    )

    AMBULANCE = (
        "AMBULANCE",
        "Ambulance",
    )

    FIRE_TRUCK = (
        "FIRE_TRUCK",
        "Fire Truck",
    )

    BOAT = (
        "BOAT",
        "Boat",
    )

    DRONE = (
        "DRONE",
        "Drone",
    )

    HELICOPTER = (
        "HELICOPTER",
        "Helicopter",
    )

class GPSStatus(models.TextChoices):

    ONLINE = (
        "ONLINE",
        "Online",
    )

    OFFLINE = (
        "OFFLINE",
        "Offline",
    )

    LOST = (
        "LOST",
        "Signal Lost",
    )


class ShiftType(models.TextChoices):

    MORNING = (
        "MORNING",
        "Morning",
    )

    AFTERNOON = (
        "AFTERNOON",
        "Afternoon",
    )

    NIGHT = (
        "NIGHT",
        "Night",
    )

    CUSTOM = (
        "CUSTOM",
        "Custom",
    )


class FuelType(models.TextChoices):

    PETROL = (
        "PETROL",
        "Petrol",
    )

    DIESEL = (
        "DIESEL",
        "Diesel",
    )

    ELECTRIC = (
        "ELECTRIC",
        "Electric",
    )

    HYBRID = (
        "HYBRID",
        "Hybrid",
    )


class EquipmentStatus(models.TextChoices):

    AVAILABLE = (
        "AVAILABLE",
        "Available",
    )

    ASSIGNED = (
        "ASSIGNED",
        "Assigned",
    )

    DAMAGED = (
        "DAMAGED",
        "Damaged",
    )

    LOST = (
        "LOST",
        "Lost",
    )

    RETIRED = (
        "RETIRED",
        "Retired",
    )


class EquipmentType(models.TextChoices):

    RADIO = (
        "RADIO",
        "Radio",
    )

    BODY_CAMERA = (
        "BODY_CAMERA",
        "Body Camera",
    )

    MEDICAL_KIT = (
        "MEDICAL_KIT",
        "Medical Kit",
    )

    FIRE_EXTINGUISHER = (
        "FIRE_EXTINGUISHER",
        "Fire Extinguisher",
    )

    FLASHLIGHT = (
        "FLASHLIGHT",
        "Flashlight",
    )

    TABLET = (
        "TABLET",
        "Tablet",
    )

    DRONE_CONTROLLER = (
        "DRONE_CONTROLLER",
        "Drone Controller",
    )

    GPS_DEVICE = (
        "GPS_DEVICE",
        "GPS Device",
    )

    OTHER = (
        "OTHER",
        "Other",
    )


class CheckpointStatus(models.TextChoices):

    PENDING = (
        "PENDING",
        "Pending",
    )

    ARRIVED = (
        "ARRIVED",
        "Arrived",
    )

    DEPARTED = (
        "DEPARTED",
        "Departed",
    )

    MISSED = (
        "MISSED",
        "Missed",
    )


class GeofenceEvent(models.TextChoices):

    ENTER = (
        "ENTER",
        "Entered",
    )

    EXIT = (
        "EXIT",
        "Exited",
    )

class MaintenanceStatus(models.TextChoices):

    SCHEDULED = (
        "SCHEDULED",
        "Scheduled",
    )

    IN_PROGRESS = (
        "IN_PROGRESS",
        "In Progress",
    )

    COMPLETED = (
        "COMPLETED",
        "Completed",
    )

    CANCELLED = (
        "CANCELLED",
        "Cancelled",
    )


class MissionOutcome(models.TextChoices):

    SUCCESS = (
        "SUCCESS",
        "Success",
    )

    PARTIAL = (
        "PARTIAL",
        "Partial",
    )

    FAILED = (
        "FAILED",
        "Failed",
    )

    ABORTED = (
        "ABORTED",
        "Aborted",
    )


