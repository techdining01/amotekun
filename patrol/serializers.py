from rest_framework import serializers

from .models import (
    Vehicle,
    VehicleType,
    PatrolTeam,
    PatrolMembership,
    VehicleAssignment,
    PatrolMission,
    PatrolCheckpoint,
    GPSPosition,
    PatrolEquipment,
    EquipmentAssignment,
    PatrolShift,
)

class VehicleTypeSerializer(serializers.ModelSerializer):

    class Meta:

        model = VehicleType

        fields = "__all__"


class VehicleSerializer(serializers.ModelSerializer):

    vehicle_type_name = serializers.CharField(
        source="vehicle_type.name",
        read_only=True,
    )

    agency_name = serializers.CharField(
        source="agency.name",
        read_only=True,
    )

    class Meta:

        model = Vehicle

        fields = (

            "id",

            "agency",

            "agency_name",

            "vehicle_type",

            "vehicle_type_name",

            "registration_number",

            "make",

            "model",

            "color",

            "year",

            "fuel_type",

            "status",

            "tracker_id",

            "created_at",

        )


class PatrolMembershipSerializer(serializers.ModelSerializer):

    user = serializers.CharField(
        source="personnel.user.get_full_name",
        read_only=True,
    )

    rank = serializers.CharField(
        source="personnel.rank.name",
        read_only=True,
    )

    class Meta:

        model = PatrolMembership

        fields = (

            "id",

            "user",

            "rank",

            "joined_at",

            "is_team_lead",

        )


class PatrolTeamSerializer(serializers.ModelSerializer):

    commander = serializers.StringRelatedField()

    agency = serializers.StringRelatedField()

    member_count = serializers.SerializerMethodField()

    members = PatrolMembershipSerializer(

        source="memberships",

        many=True,

        read_only=True,

    )

    class Meta:

        model = PatrolTeam

        fields = (

            "id",

            "name",

            "agency",

            "commander",

            "team_type",

            "status",

            "active",

            "member_count",

            "members",

        )

    def get_member_count(self, obj):

        return obj.memberships.count()


class VehicleAssignmentSerializer(serializers.ModelSerializer):

    vehicle = VehicleSerializer(
        read_only=True,
    )

    class Meta:

        model = VehicleAssignment

        fields = (

            "id",

            "vehicle",

            "assigned_at",

            "released_at",

            "active",

        )


class PatrolCheckpointSerializer(serializers.ModelSerializer):

    class Meta:

        model = PatrolCheckpoint

        fields = "__all__"


class GPSSerializer(serializers.ModelSerializer):

    latitude = serializers.SerializerMethodField()

    longitude = serializers.SerializerMethodField()

    class Meta:

        model = GPSPosition

        fields = (

            "id",

            "latitude",

            "longitude",

            "heading",

            "speed",

            "accuracy",

            "recorded_at",

        )

    def get_latitude(self, obj):

        return obj.location.y

    def get_longitude(self, obj):

        return obj.location.x



class PatrolMissionSerializer(serializers.ModelSerializer):

    team = PatrolTeamSerializer(
        source="patrol_team",
        read_only=True,
    )

    vehicle = VehicleAssignmentSerializer(
        source="vehicle_assignment",
        read_only=True,
    )

    checkpoints = PatrolCheckpointSerializer(

        many=True,

        read_only=True,

    )

    latest_position = serializers.SerializerMethodField()

    incident_title = serializers.CharField(

        source="incident.title",

        read_only=True,

    )

    class Meta:

        model = PatrolMission

        fields = (

            "id",

            "dispatch",

            "incident",

            "incident_title",

            "team",

            "vehicle",

            "priority",

            "status",

            "started_at",

            "completed_at",

            "outcome",

            "notes",

            "latest_position",

            "checkpoints",

        )

    def get_latest_position(self, obj):

        gps = obj.gps_points.first()

        if not gps:

            return None

        return GPSSerializer(gps).data


class PatrolEquipmentSerializer(serializers.ModelSerializer):

    class Meta:

        model = PatrolEquipment

        fields = "__all__"


class EquipmentAssignmentSerializer(serializers.ModelSerializer):

    equipment = PatrolEquipmentSerializer(
        read_only=True,
    )

    officer = serializers.CharField(

        source="personnel.user.get_full_name",

        read_only=True,

    )

    class Meta:

        model = EquipmentAssignment

        fields = (

            "id",

            "equipment",

            "officer",

            "assigned_at",

            "returned_at",

            "active",

        )


class PatrolShiftSerializer(serializers.ModelSerializer):

    team = serializers.StringRelatedField()

    class Meta:

        model = PatrolShift

        fields = "__all__"


class PatrolDashboardSerializer(serializers.Serializer):

    teams = serializers.IntegerField()

    active_teams = serializers.IntegerField()

    available_vehicles = serializers.IntegerField()

    active_missions = serializers.IntegerField()

    completed_today = serializers.IntegerField()



class PatrolMapSerializer(serializers.ModelSerializer):

    latitude = serializers.SerializerMethodField()

    longitude = serializers.SerializerMethodField()

    team = serializers.CharField(

        source="mission.patrol_team.name"

    )

    vehicle = serializers.CharField(

        source="vehicle.registration_number"

    )

    class Meta:

        model = GPSPosition

        fields = (

            "team",

            "vehicle",

            "latitude",

            "longitude",

            "speed",

            "heading",

            "recorded_at",

        )

    def get_latitude(self,obj):

        return obj.location.y

    def get_longitude(self,obj):

        return obj.location.x


class PatrolPredictionSerializer(serializers.Serializer):

    mission = serializers.IntegerField()

    predicted_arrival = serializers.DateTimeField()

    confidence = serializers.FloatField()

    suggested_route = serializers.JSONField()

    risk_score = serializers.FloatField()


class GeoPointMixin(serializers.Serializer):

    latitude = serializers.SerializerMethodField()

    longitude = serializers.SerializerMethodField()

    def get_latitude(self, obj):
        return obj.location.y

    def get_longitude(self, obj):
        return obj.location.x


