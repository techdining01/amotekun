from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.conf import settings
from django.utils import timezone
from django.contrib.gis.db import models 

from reports.models import State, LGA, Ward

from .choices import (
    UserRole,
    AgencyType,
    Gender,
    UserStatus,
    VerificationStatus,
    AvailabilityStatus,
   
)

from .managers import UserManager


class Agency(models.Model):

    name = models.CharField(
        max_length=120,
        unique=True,
    )

    agency_type = models.CharField(
        max_length=50,
        choices=AgencyType.choices,
        unique=True,
    )

    description = models.TextField(
        blank=True,
    )

    phone_number = models.CharField(
        max_length=30,
        blank=True,
    )

    email = models.EmailField(
        blank=True,
    )

    logo = models.ImageField(
        upload_to="agency/logos/",
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        ordering = ["name"]

    def __str__(self):

        return self.name


class User(
    AbstractBaseUser,
    PermissionsMixin,
):

    email = models.EmailField(
        unique=True,
    )

    username = models.CharField(
        max_length=50,
        unique=True,
    )

    phone_number = models.CharField(
        max_length=20,
        blank=True,
    )

    first_name = models.CharField(
        max_length=150,
    )

    last_name = models.CharField(
        max_length=150,
    )

    middle_name = models.CharField(
        max_length=150,
        blank=True,
    )

    gender = models.CharField(
        max_length=20,
        choices=Gender.choices,
        blank=True,
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True,
    )

    role = models.CharField(

        max_length=40,

        choices=UserRole.choices,

        default=UserRole.CITIZEN,

    )

    state = models.ForeignKey(

        State,

        on_delete=models.SET_NULL,

        null=True,

        blank=True,

    )

    lga = models.ForeignKey(

        LGA,

        on_delete=models.SET_NULL,

        null=True,

        blank=True,

    )

    ward = models.ForeignKey(

        Ward,

        on_delete=models.SET_NULL,

        null=True,

        blank=True,

    )


    status = models.CharField(

        max_length=30,

        choices=UserStatus.choices,

        default=UserStatus.PENDING,

    )

    verification_status = models.CharField(

        max_length=30,

        choices=VerificationStatus.choices,

        default=VerificationStatus.UNVERIFIED,

    )

    email_verified = models.BooleanField(

        default=False,

    )

    phone_verified = models.BooleanField(

        default=False,

    )

    language = models.CharField(

        max_length=20,

        default="en",

    )

    timezone = models.CharField(

        max_length=60,

        default="Africa/Lagos",

    )

    dark_mode = models.BooleanField(

        default=False,

    )

    ai_enabled = models.BooleanField(

        default=True,

    )

    notification_enabled = models.BooleanField(

        default=True,

    )

    last_seen = models.DateTimeField(

        null=True,

        blank=True,

    )

    last_login_ip = models.GenericIPAddressField(

        null=True,

        blank=True,

    )

    failed_login_attempts = models.PositiveIntegerField(

        default=0,

    )

    is_staff = models.BooleanField(

        default=False,

    )

    is_active = models.BooleanField(

        default=True,

    )

    created_at = models.DateTimeField(

        auto_now_add=True,

    )

    updated_at = models.DateTimeField(

        auto_now=True,

    )

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = [

        "username",

    ]

    objects = UserManager()

    class Meta:

        ordering = [

            "first_name",

        ]

    def __str__(self):

        return self.get_full_name()

    def get_full_name(self):

        return f"{self.first_name} {self.last_name}"

    @property
    def is_online(self):

        if not self.last_seen:

            return False

        return (

            timezone.now() - self.last_seen

        ).seconds < 300


class UserProfile(models.Model):

    user = models.OneToOneField(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE,

        related_name="profile",

    )

    address = models.TextField(blank=True)

    occupation = models.CharField(

        max_length=150,

        blank=True,

    )

    nationality = models.CharField(

        max_length=100,

        default="Nigeria",

    )

    bio = models.TextField(blank=True)

    emergency_contact_name = models.CharField(

        max_length=200,

        blank=True,

    )

    emergency_contact_phone = models.CharField(

        max_length=20,

        blank=True,

    )

    created_at = models.DateTimeField(

        auto_now_add=True,

    )

    updated_at = models.DateTimeField(

        auto_now=True,

    )

    def __str__(self):

        return self.user.get_full_name()


class PersonnelAssignment(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="assignments",
    )

    agency = models.ForeignKey(
        "accounts.Agency",
        on_delete=models.CASCADE,
    )

    station = models.ForeignKey(
        "stations.PoliceStation",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    state = models.ForeignKey(
        "reports.State",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    lga = models.ForeignKey(
        "reports.LGA",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    role = models.CharField(
        max_length=40,
        choices=UserRole.choices,
    )

    badge_number = models.CharField(
        max_length=50,
        blank=True,
    )

    employee_id = models.CharField(
        max_length=50,
        blank=True,
    )

    is_primary = models.BooleanField(
        default=True,
    )

    started_at = models.DateField()

    ended_at = models.DateField(
        null=True,
        blank=True,
    )

    @property
    def employee_number(self):
        if not self.employee_id:
            import secrets
            return f'({self.state.name[:3]}-{secrets.token_hex(4)}).upper()'
        return self.employee_id


    def __str__(self):

        return f"{self.user.get_full_name()} - {self.agency.name}"


class NotificationPreference(models.Model):

    user = models.OneToOneField(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE,

        related_name="notification_preferences",

    )

    email = models.BooleanField(default=True)

    sms = models.BooleanField(default=False)

    push = models.BooleanField(default=True)

    in_app = models.BooleanField(default=True)

    incident_updates = models.BooleanField(default=True)

    patrol_updates = models.BooleanField(default=True)

    dispatch_updates = models.BooleanField(default=True)

    security_alerts = models.BooleanField(default=True)

    ai_predictions = models.BooleanField(default=True)

    def __str__(self):

        return self.user.get_full_name()


class ResponderStatus(models.Model):

    responder = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="responder_status",
    )

    availability = models.CharField(
        max_length=30,
        choices=AvailabilityStatus.choices,
    )

    current_patrol = models.ForeignKey(
        "patrol.PatrolMission",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="responder_statuses",
    )

    current_vehicle = models.ForeignKey(
        "patrol.Vehicle",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    current_dispatch = models.ForeignKey(
        "dispatch.Dispatch",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    last_location = models.PointField(
        srid=4326,
        geography=True,
        null=True,
        blank=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )


class EmergencyContact(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="emergency_contacts",
    )

    full_name = models.CharField(max_length=150)

    phone_number = models.CharField(max_length=20)

    relationship = models.CharField(max_length=80)

    is_primary = models.BooleanField(default=False)


class UserDevice(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="devices",
    )

    device_name = models.CharField(max_length=100)

    platform = models.CharField(max_length=40)

    device_id = models.CharField(max_length=255)

    fcm_token = models.TextField(blank=True)

    last_seen = models.DateTimeField(auto_now=True)


class UserAuditLog(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    action = models.CharField(max_length=200)

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )