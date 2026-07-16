from django.contrib.auth import get_user_model
import accounts.models as models


def get_user():
    return get_user_model()


class UserSelector:

    @staticmethod
    def by_id(user_id):
        User = get_user()
        return (
            User.objects
            .select_related(
                "profile",
                "notification_preferences",
            )
            .get(pk=user_id)
        )

    @staticmethod
    def responders():
        User = get_user()
        return (
            User.objects.filter(
                role="RESPONDER",
            )
            .select_related(
                "profile",
            )
        )

    @staticmethod
    def citizens():
        User = get_user()
        return User.objects.filter(
            role="CITIZEN",
        )

    @staticmethod
    def online():
        User = get_user()
        return User.objects.filter(
            is_active=True,
        )


class AgencySelector:

    @staticmethod
    def active():

        return models.Agency.objects.filter(
            is_active=True,
        )

    @staticmethod
    def with_users():

        return models.Agency.objects.prefetch_related(
            "users",
        )

class PersonnelSelector:

    @staticmethod
    def current_assignments():

        return models.PersonnelAssignment.objects.filter(
            ended_at__isnull=True,
        ).select_related(
            "user",
            "agency",
            "station",
            "state",
            "lga",
        )