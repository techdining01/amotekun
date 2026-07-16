from django.utils import timezone
from .models import Dispatch, DispatchHistory
from django.db import transaction



class DispatchService:

    @staticmethod
    @transaction.atomic
    def create_dispatch(
        incident,
        dispatcher,
        priority="MEDIUM",
        station=None,
    ):
        dispatch = Dispatch.objects.create(
            incident=incident,
            dispatcher=dispatcher,
            priority=priority,
            station=station,
            state=incident.state,
            lga=incident.lga,
            location=incident.geometry,
        )

        return dispatch


    @staticmethod
    @transaction.atomic
    def assign_team(
        dispatch,
        patrol_team,
        vehicle=None,
    ):
        dispatch.patrol_team = patrol_team
        dispatch.vehicle = vehicle

        dispatch.transition_to("dispatched")

        dispatch.save()

        return dispatch


    @staticmethod
    @transaction.atomic
    def accept_dispatch(
        dispatch,
        responder,
    ):
        dispatch.accepted_by = responder

        dispatch.accepted_at = timezone.now()

        dispatch.transition_to("accepted")

        dispatch.save()

        return dispatch


    @staticmethod
    @transaction.atomic
    def start_response(dispatch):

        dispatch.started_at = timezone.now()

        dispatch.transition_to("in_progress")

        dispatch.save()

        return dispatch


    @staticmethod
    @transaction.atomic
    def resolve_dispatch(
        dispatch,
        resolution_note="",
    ):
        dispatch.resolution_notes = resolution_note

        dispatch.resolved_at = timezone.now()

        dispatch.transition_to("resolved")

        dispatch.save()

        return dispatch


class DispatchHistoryService:

    @staticmethod
    def log(
        dispatch,
        action,
        user=None,
        note="",
    ):
        DispatchHistory.objects.create(
            dispatch=dispatch,
            user=user,
            action=action,
            note=note,
        )
