from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Dispatch
from .serializers import DispatchSerializer


class DispatchViewSet(viewsets.ModelViewSet):
    queryset = Dispatch.objects.select_related(
        "incident",
        "police_station",
        "amotekun_station",
        "assigned_officer",
        "assigned_dispatcher",
    )

    serializer_class = DispatchSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"])
    def active(self, request):

        queryset = self.get_queryset().exclude(
            status__in=[
                "resolved",
                "cancelled",
            ]
        )

        serializer = self.get_serializer(
            queryset,
            many=True,
        )

        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def pending(self, request):

        queryset = self.get_queryset().filter(
            status="pending"
        )

        serializer = self.get_serializer(
            queryset,
            many=True,
        )

        return Response(serializer.data)


    @action(
        detail=False,
        methods=["get"],
    )
    def my_assignments(self, request):

        queryset = self.get_queryset().filter(
            assigned_officer=request.user
        )

        serializer = self.get_serializer(
            queryset,
            many=True,
        )

        return Response(serializer.data)


    @action(
        detail=True,
        methods=["post"],
    )
    def dispatch(self, request, pk=None):

        dispatch = self.get_object()

        dispatch.transition_to(
            "dispatched"
        )

        return Response(
            {
                "status": "dispatched"
            }
        )

    @action(
        detail=True,
        methods=["post"],
    )
    def start(self, request, pk=None):

        dispatch = self.get_object()

        dispatch.transition_to("in_progress")

        return Response({"status": "in_progress"})

    @action(
        detail=True,
        methods=["post"],
    )
    def cancel(self, request, pk=None):

        reason = request.data.get(
            "reason",
            "",
        )

        dispatch = self.get_object()

        dispatch.cancel(reason)

        return Response({"status": "cancelled"})

    @action(
        detail=True,
        methods=["post"],
    )
    def assign_officer(self, request, pk=None):

        dispatch = self.get_object()

        officer_id = request.data.get("officer_id")

        from accounts.models import User

        officer = User.objects.get(pk=officer_id)

        dispatch.assign_officer(officer)

        return Response({"status": "assigned"})


    @action(
        detail=True,
        methods=["get"],
    )
    def nearby_units(self, request, pk=None):

        dispatch = self.get_object()

        from patrol.services import PatrolService

        units = PatrolService.nearest_units(
            dispatch.incident.geometry
        )

        return Response(units)
