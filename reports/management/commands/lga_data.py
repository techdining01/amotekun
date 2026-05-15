import json

from django.core.management.base import BaseCommand

from django.contrib.gis.geos import GEOSGeometry

from reports.models import LGA


class Command(BaseCommand):
    help = "Load Nigerian LGAs into PostGIS"

    def handle(self, *args, **kwargs):

        filepath = "static/data/LGA_data.geojson"

        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)

        created_count = 0

        for feature in data["features"]:
            props = feature["properties"]

            geometry = feature["geometry"]

            lga_name = props["shapeName"]

            geom = GEOSGeometry(json.dumps(geometry))

            lga, created = LGA.objects.get_or_create(
                name=lga_name, defaults={"geometry": geom}
            )

            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(f"Successfully loaded {created_count} LGAs")
        )
