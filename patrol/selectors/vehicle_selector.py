from ..models import Vehicle

class VehicleSelector:

    @staticmethod
    def available():

        return Vehicle.objects.filter(
            status="AVAILABLE",
        )

    @staticmethod
    def assigned():

        return Vehicle.objects.filter(
            status="ASSIGNED",
        )

    @staticmethod
    def by_registration(number):

        return Vehicle.objects.get(
            registration_number=number,
        )
