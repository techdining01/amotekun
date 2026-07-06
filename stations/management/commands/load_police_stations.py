import json
from pathlib import Path
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from stations.models import PoliceStation


class Command(BaseCommand):
    help = "Load Nigerian police stations from GeoJSON into the database"

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default='static/data/NGA_Police_Stations.geojson',
            help='Path to the police stations GeoJSON file'
        )

    def handle(self, *args, **kwargs):
        filepath = Path(kwargs['file'])
        if not filepath.exists():
            self.stdout.write(
                self.style.ERROR(f"File not found: {filepath}")
            )
            return

        with open(filepath, encoding='utf-8') as f:
            data = json.load(f)

        created_count = 0
        updated_count = 0

        for feature in data.get("features", []):
            props = feature["properties"]
            geometry = feature["geometry"]

            # Extract data
            name = props.get("plc_st_nam", "").strip()
            lga = props.get("lganame", "").strip()
            state = props.get("statename", "").strip()
            # We can use wardname as address or build address from ward/lga/state
            address = f"{props.get('wardname', '')}, {lga}, {state}".strip()

            # Create point geometry
            if geometry and geometry.get("type") == "Point" and geometry.get("coordinates"):
                lon, lat = geometry["coordinates"]
                location = Point(lon, lat, srid=4326)
            else:
                location = None

            # Get or create police station
            if name:
                station, created = PoliceStation.objects.get_or_create(
                    name=name,
                    defaults={
                        'address': address,
                        'state': state,
                        'lga': lga,
                        'location': location
                    }
                )

                if created:
                    created_count += 1
                    self.stdout.write(f"Created: {name}")
                else:
                    # Update existing station
                    station.address = address
                    station.state = state
                    station.lga = lga
                    station.location = location
                    station.save()
                    updated_count += 1
                    self.stdout.write(f"Updated: {name}")

        self.stdout.write(
            self.style.SUCCESS(f"Successfully processed {created_count} created, {updated_count} updated police stations")
        )
