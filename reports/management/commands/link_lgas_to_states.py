from django.core.management.base import BaseCommand

from reports.models import State, LGA


class Command(BaseCommand):
    help = "Link LGAs to states using spatial containment"

    def handle(self, *args, **kwargs):

        updated = 0

        lgas = LGA.objects.all()

        for lga in lgas:
            state = State.objects.filter(
                geometry__contains=lga.geometry.centroid
            ).first()

            if state:
                lga.state = state

                lga.save()

                updated += 1

                self.stdout.write(f"Linked {lga.name} -> {state.name}")

        self.stdout.write(self.style.SUCCESS(f"Successfully linked {updated} LGAs"))
