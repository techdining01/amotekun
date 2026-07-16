from django.contrib.auth import authenticate, get_user_model
from django.db import transaction
from django.utils import timezone
from .selectors import UserSelector

# from allauth.account.utils import send_email_confirmation


def get_user():
    return get_user_model()


class AuthenticationService:

    @staticmethod
    def login(request, email, password):

        user = authenticate(
            request=request,
            username=email,
            password=password,
        )

        return user

    @staticmethod
    def send_verification_email(request, user):

        send_email_confirmation(
            request,
            user,
        )

class AccountService:

    @staticmethod
    @transaction.atomic
    def create_user(**validated_data):
        User = get_user()
        password = validated_data.pop("password")

        user = User.objects.create_user(
            **validated_data
        )

        user.set_password(password)

        user.save()

        return user

    @staticmethod
    @transaction.atomic
    def update_profile(user, data):

        profile = user.profile

        for key, value in data.items():

            setattr(profile, key, value)

        profile.save()

        return profile

    @staticmethod
    def activate(user):

        user.is_active = True

        user.status = "ACTIVE"

        user.save()

        return user


    @staticmethod
    def suspend(user):

        user.status = "SUSPENDED"

        user.save()


class RoleService:

    @staticmethod
    def assign(user, role):

        user.role = role

        user.save()

        return user


    @staticmethod
    def assign_personnel(user, **kwargs):
        from .models import PersonnelAssignment
        PersonnelAssignment.objects.create(

            user=user,

            **kwargs,

        )

class DashboardRouterService:

    ROUTES = {

        "SUPER_ADMIN":

            "dashboard:super-admin",

        "PLATFORM_ADMIN":

            "dashboard:admin",

        "STATE_COMMANDER":

            "dashboard:state",

        "LGA_COMMANDER":

            "dashboard:lga",

        "STATION_COMMANDER":

            "dashboard:station",

        "DISPATCHER":

            "dashboard:dispatcher",

        "PATROL_SUPERVISOR":

            "dashboard:patrol-supervisor",

        "PATROL_OFFICER":

            "dashboard:patrol",

        "RESPONDER":

            "dashboard:responder",

        "ANALYST":

            "dashboard:analyst",

        "CCTV_OPERATOR":

            "dashboard:cctv",

        "EMERGENCY_OPERATOR":

            "dashboard:emergency",

        "CITIZEN":

            "dashboard:citizen",

    }

    @classmethod
    def get_dashboard(

        cls,

        user,

    ):

        return cls.ROUTES.get(

            user.role,

            "dashboard:citizen",

        )

class PermissionService:

    @staticmethod
    def is_commander(user):

        return user.role in [

            "STATE_COMMANDER",

            "LGA_COMMANDER",

            "STATION_COMMANDER",

        ]

    @staticmethod
    def is_admin(user):

        return user.role in [

            "SUPER_ADMIN",

            "PLATFORM_ADMIN",

        ]

    @staticmethod
    def can_dispatch(user):

        return user.role in [

            "DISPATCHER",

            "STATE_COMMANDER",

            "STATION_COMMANDER",

        ]


class ProfileService:

    @staticmethod
    def mark_online(

        user,

    ):

        user.last_seen = timezone.now()

        user.save(
            update_fields=[
                "last_seen",
            ]
        )


    @staticmethod
    def mark_offline(

        user,

    ):

        user.last_seen = timezone.now()

        user.save()


class ResponderService:

    @staticmethod
    def current_status(

        responder,

    ):

        return responder.responder_status


    @staticmethod
    def set_available(

        responder,

    ):

        status = responder.responder_status

        status.availability = "AVAILABLE"

        status.save()

        return status

    @staticmethod
    def set_on_dispatch(

        responder,

        dispatch,

    ):

        status = responder.responder_status

        status.availability = "ON_DISPATCH"

        status.current_dispatch = dispatch

        status.save()

        return status


class NotificationPreferenceService:

    @staticmethod
    def update(

        user,

        **kwargs,

    ):

        preferences = user.notification_preferences

        for key, value in kwargs.items():

            setattr(

                preferences,

                key,

                value,

            )

        preferences.save()

        return preferences


class UserStatisticsService:

    @staticmethod
    def summary():
        User = get_user()
        return {

            "users":

                User.objects.count(),

            "responders":

                User.objects.responders().count(),

            "citizens":

                User.objects.citizens().count(),

            "online":

                UserSelector.online().count(),

        }