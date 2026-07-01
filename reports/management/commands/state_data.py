import json

from django.core.management.base import BaseCommand

from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import MultiPolygon

from reports.models import State


class Command(BaseCommand):
    help = "Load Nigerian states into PostGIS"

    def handle(self, *args, **kwargs):

        filepath = "static/data/geoBoundaries-NGA-ADM1_simplified.geojson"

        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)

        created_count = 0

        for feature in data["features"]:
            props = feature["properties"]

            geometry = feature["geometry"]

            state_name = props["shapeName"]

            geom = GEOSGeometry(json.dumps(geometry))
            if geom.geom_type == 'Polygon':
                geom = MultiPolygon(geom)

            state, created = State.objects.get_or_create(
                name=state_name, defaults={"geometry": geom}
            )

            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(f"Successfully loaded {created_count} states")
        )
