from patrol.services.assignment import (
    VehicleAssignmentService
)

from patrol.services.mission import MissionService


class PatrolService:

    @staticmethod
    def dispatch(

        dispatch,

        incident,

        team,

        vehicle,

        priority,

    ):

        assignment = VehicleAssignmentService.assign(

            vehicle,

            team,

        )

        mission = MissionService.create_from_dispatch(
            dispatch,
            incident,
            team,
            assignment,
            priority,
        )

        return mission