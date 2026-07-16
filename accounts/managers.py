from django.contrib.auth.base_user import BaseUserManager
from django.db import transaction

from .services import (
    AccountService,
    AuthenticationService,
    DashboardRouterService,
    NotificationPreferenceService,
    ProfileService,
    ResponderService,
    RoleService,
)

from .selectors import UserSelector


class UserManager(BaseUserManager):

    use_in_migrations = True

    def create_user(
        self,
        email,
        password=None,
        **extra_fields,
    ):
        if not email:
            raise ValueError("Email is required.")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            **extra_fields,
        )

        user.set_password(password)

        user.save(using=self._db)

        return user


    def create_superuser(
        self,
        email,
        password,
        **extra_fields,
    ):
        extra_fields.setdefault(
            "is_staff",
            True,
        )

        extra_fields.setdefault(
            "is_superuser",
            True,
        )

        extra_fields.setdefault(
            "is_active",
            True,
        )

        extra_fields.setdefault(
            "role",
            "SUPER_ADMIN",
        )

        return self.create_user(
            email,
            password,
            **extra_fields,
        )

    def active(self):
        return self.filter(
            is_active=True,
        )

    def responders(self):
        return self.filter(
            role="RESPONDER",
        )

    def citizens(self):
        return self.filter(
            role="CITIZEN",
        )

    def commanders(self):
        return self.filter(
            role__in=[
                "STATE_COMMANDER",
                "LGA_COMMANDER",
                "STATION_COMMANDER",
            ]
        )


class AccountManager:

    @staticmethod
    @transaction.atomic
    def register_user(validated_data):

        user = AccountService.create_user(
            **validated_data,
        )

        AuthenticationService.send_verification_email(
            None,
            user,
        )

        return user


    @staticmethod
    @transaction.atomic
    def complete_profile(

        user,

        profile_data,

    ):

        return AccountService.update_profile(

            user,

            profile_data,

        )

    @staticmethod
    def suspend(user):

        AccountService.suspend(

            user,

        )

    @staticmethod
    def activate(user):

        AccountService.activate(

            user,

        )

class DashboardManager:

    @staticmethod
    def dashboard_url(user):

        return DashboardRouterService.get_dashboard(
            user,
        )


class ResponderManager:

    @staticmethod
    def available(responder):

        return ResponderService.set_available(responder)


    @staticmethod
    def dispatch(responder, dispatch):

        return ResponderService.set_on_dispatch(

            responder,

            dispatch,

        )


class ProfileManager:

    @staticmethod
    def update(user, data):

        return AccountService.update_profile(user, data)


class NotificationManager:

    @staticmethod
    def update_preferences(user, **kwargs):

        return NotificationPreferenceService.update(

            user,

            **kwargs,

        )

    

class UserQueryManager:

    @staticmethod
    def by_id(user_id):

        return UserSelector.by_id(user_id)

    @staticmethod
    def responders():

        return UserSelector.responders()

    @staticmethod
    def citizens():

        return UserSelector.citizens()