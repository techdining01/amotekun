from django.db import models


class UserRole(models.TextChoices):
    SUPER_ADMIN = "SUPER_ADMIN", "Super Admin"
    PLATFORM_ADMIN = "PLATFORM_ADMIN", "Platform Admin"

    STATE_COMMANDER = "STATE_COMMANDER", "State Commander"
    LGA_COMMANDER = "LGA_COMMANDER", "LGA Commander"
    STATION_COMMANDER = "STATION_COMMANDER", "Station Commander"

    DISPATCHER = "DISPATCHER", "Dispatcher"

    PATROL_SUPERVISOR = "PATROL_SUPERVISOR", "Patrol Supervisor"
    PATROL_OFFICER = "PATROL_OFFICER", "Patrol Officer"

    RESPONDER = "RESPONDER", "Responder"

    ANALYST = "ANALYST", "Analyst"
    AUDITOR = "AUDITOR", "Auditor"

    CCTV_OPERATOR = "CCTV_OPERATOR", "CCTV Operator"

    EMERGENCY_OPERATOR = "EMERGENCY_OPERATOR", "Emergency Operator"

    AGENCY_STAFF = "AGENCY_STAFF", "Agency Staff"

    CITIZEN = "CITIZEN", "Citizen"


class AgencyType(models.TextChoices):
    POLICE = "POLICE", "Police"

    AMOTEKUN = "AMOTEKUN", "Amotekun"

    FRSC = "FRSC", "Federal Road Safety Corps"

    NSCDC = "NSCDC", "Nigeria Security and Civil Defence Corps"

    FIRE = "FIRE", "Fire Service"

    LASTMA = "LASTMA", "LASTMA"

    NEMA = "NEMA", "NEMA"

    LASEMA = "LASEMA", "LASEMA"

    EMS = "EMS", "Emergency Medical Service"

    VOLUNTEER = "VOLUNTEER", "Volunteer"

    PRIVATE_SECURITY = "PRIVATE_SECURITY", "Private Security"


class Gender(models.TextChoices):
    MALE = "MALE", "Male"

    FEMALE = "FEMALE", "Female"

    OTHER = "OTHER", "Other"


class UserStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"

    ACTIVE = "ACTIVE", "Active"

    SUSPENDED = "SUSPENDED", "Suspended"

    BLOCKED = "BLOCKED", "Blocked"

    DEACTIVATED = "DEACTIVATED", "Deactivated"


class VerificationStatus(models.TextChoices):
    UNVERIFIED = "UNVERIFIED", "Unverified"

    PENDING = "PENDING", "Pending"

    VERIFIED = "VERIFIED", "Verified"

    REJECTED = "REJECTED", "Rejected"


class Shift(models.TextChoices):
    MORNING = "MORNING", "Morning"

    AFTERNOON = "AFTERNOON", "Afternoon"

    NIGHT = "NIGHT", "Night"

    FLEXIBLE = "FLEXIBLE", "Flexible"


class AvailabilityStatus(models.TextChoices):
    AVAILABLE = "AVAILABLE", "Available"

    ON_PATROL = "ON_PATROL", "On Patrol"

    ON_DISPATCH = "ON_DISPATCH", "On Dispatch"

    OFF_DUTY = "OFF_DUTY", "Off Duty"

    LEAVE = "LEAVE", "Leave"

    TRAINING = "TRAINING", "Training"


