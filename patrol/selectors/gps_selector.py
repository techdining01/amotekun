from ..models import GPSPosition

class GPSSelector:

    @staticmethod
    def latest(mission):

        return GPSPosition.objects.filter(
            mission=mission,
        ).first()

    @staticmethod
    def history(mission):

        return GPSPosition.objects.filter(
            mission=mission,
        )

    @staticmethod
    def latest_for_vehicle(vehicle):

        return GPSPosition.objects.filter(
            vehicle=vehicle,
        ).first()
