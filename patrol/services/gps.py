from ..models import GPSPosition


class GPSService:

    @staticmethod
    def record(

        mission,

        vehicle,

        point,

        heading,

        speed,

        accuracy,

    ):

        return GPSPosition.objects.create(

            mission=mission,

            vehicle=vehicle,

            location=point,

            heading=heading,

            speed=speed,

            accuracy=accuracy,

        )