from django.contrib.auth import get_user_model
from rest_framework import serializers
from allauth.account.adapter import get_adapter

from ..models import (
    Agency,
    UserProfile,
    NotificationPreference,
    PersonnelAssignment,
    ResponderStatus,
)

User = get_user_model()


class AgencySerializer(serializers.ModelSerializer):

    class Meta:

        model = Agency

        fields = "__all__"


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:

        model = UserProfile

        exclude = [
            "user",
        ]


class NotificationPreferenceSerializer(serializers.ModelSerializer):

    class Meta:

        model = NotificationPreference

        exclude = [
            "user",
        ]

class PersonnelAssignmentSerializer(serializers.ModelSerializer):

    agency_name = serializers.CharField(
        source="agency.name",
        read_only=True,
    )

    station_name = serializers.CharField(
        source="station.name",
        read_only=True,
    )

    class Meta:

        model = PersonnelAssignment

        fields = "__all__"


class ResponderStatusSerializer(serializers.ModelSerializer):

    patrol = serializers.CharField(
        source="current_patrol.name",
        read_only=True,
    )

    vehicle = serializers.CharField(
        source="current_vehicle.registration_number",
        read_only=True,
    )

    class Meta:

        model = ResponderStatus

        fields = "__all__"



class UserListSerializer(serializers.ModelSerializer):

    full_name = serializers.CharField(
        source="get_full_name",
        read_only=True,
    )

    agency = serializers.CharField(
        source="agency.name",
        read_only=True,
    )

    class Meta:

        model = User

        fields = [

            "id",

            "avatar",

            "full_name",

            "email",

            "role",

            "agency",

            "status",

            "is_active",

        ]


class UserDetailSerializer(serializers.ModelSerializer):

    profile = UserProfileSerializer(
        read_only=True,
    )

    notification_preferences = NotificationPreferenceSerializer(
        read_only=True,
    )

    assignments = PersonnelAssignmentSerializer(
        many=True,
        read_only=True,
    )

    responder_status = ResponderStatusSerializer(
        read_only=True,
    )

    class Meta:

        model = User

        exclude = [

            "password",

            "groups",

            "user_permissions",

        ]


class RegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
    )

    confirm_password = serializers.CharField(
        write_only=True,
    )

    class Meta:

        model = User

        fields = [

            "email",

            "username",

            "password",

            "confirm_password",

            "first_name",

            "last_name",

            "phone_number",

        ]

    def validate(self, attrs):

        if attrs["password"] != attrs["confirm_password"]:

            raise serializers.ValidationError(

                "Passwords do not match."

            )

        return attrs

    def create(self, validated_data):

        validated_data.pop(

            "confirm_password",

        )

        user = User.objects.create_user(

            **validated_data,

        )

        return user


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()

    password = serializers.CharField(
        write_only=True,
    )


class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField()

    new_password = serializers.CharField()

    confirm_password = serializers.CharField()

    def validate(self, attrs):

        if attrs["new_password"] != attrs["confirm_password"]:

            raise serializers.ValidationError(

                "Passwords do not match."

            )

        get_adapter().clean_password(

            attrs["new_password"]

        )

        return attrs


class ResetPasswordSerializer(serializers.Serializer):

    email = serializers.EmailField()


class AssignRoleSerializer(serializers.Serializer):

    role = serializers.CharField()

    agency = serializers.IntegerField()

    state = serializers.IntegerField(
        required=False,
    )

    lga = serializers.IntegerField(
        required=False,
    )

    station = serializers.IntegerField(
        required=False,
    )


class UpdateProfileSerializer(serializers.ModelSerializer):

    class Meta:

        model = UserProfile

        exclude = [

            "user",

        ]


class UserSearchSerializer(serializers.ModelSerializer):

    full_name = serializers.CharField(
        source="get_full_name",
    )

    class Meta:

        model = User

        fields = [

            "id",

            "full_name",

            "email",

            "role",

            "avatar",

        ]


class OnlineUserSerializer(serializers.ModelSerializer):

    full_name = serializers.CharField(
        source="get_full_name",
    )

    class Meta:

        model = User

        fields = [

            "id",

            "full_name",

            "last_seen",

            "role",

        ]