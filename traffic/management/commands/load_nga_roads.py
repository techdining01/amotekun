import csv
from pathlib import Path
from io import StringIO
from django.core.management.base import BaseCommand
from traffic.models import Road


class Command(BaseCommand):
    help = "Load Nigerian roads from NGA_roads.csv"

    # Map Overture/OSM classes to our Road model's ROAD_TYPES
    ROAD_CLASS_MAP = {
        "motorway": "highway",
        "trunk": "highway",
        "primary": "arterial",
        "secondary": "arterial",
        "tertiary": "collector",
        "unclassified": "local",
        "residential": "local",
        "service": "local",
        "track": "local",
        "path": "local",
    }

    def clean_string(self, value):
        """Clean up string values: remove NUL characters, strip whitespace."""
        if not isinstance(value, str):
            return value
        return value.replace("\x00", "").strip()

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            default="static/data/NGA_roads.csv",
            help="Path to NGA_roads.csv file",
        )

    def handle(self, *args, **options):
        filepath = Path(options["file"])
        if not filepath.exists():
            self.stdout.write(
                self.style.ERROR(f"File not found: {filepath}")
            )
            return

        created_count = 0
        updated_count = 0
        skipped_count = 0

        # Read entire file and remove NUL characters first
        with open(filepath, encoding="utf-8", errors="replace") as f:
            content = f.read().replace("\x00", "")

        # Parse cleaned content as CSV
        csv_file = StringIO(content)
        reader = csv.DictReader(csv_file)

        for row in reader:
            # Extract and clean data from CSV
            source_id = self.clean_string(row.get("source_id", ""))
            overture_class = self.clean_string(row.get("class", "")).lower()
            speed_estimate = self.clean_string(row.get("speed_estimate", None))
            names = self.clean_string(row.get("names", ""))

            # Skip if no source_id (unique identifier)
            if not source_id:
                skipped_count += 1
                continue

            # Map road class
            road_type = self.ROAD_CLASS_MAP.get(overture_class, "local")

            # Parse speed limit
            speed_limit = None
            if speed_estimate:
                try:
                    speed_limit = int(float(speed_estimate))
                except (ValueError, TypeError):
                    pass

            # Get name from names column or use None
            name = names if names else None

            # Get or create Road object using source_id
            road, created = Road.objects.update_or_create(
                source_id=source_id,
                defaults={
                    "name": name,
                    "road_type": road_type,
                    "speed_limit": speed_limit,
                }
            )

            if created:
                created_count += 1
                self.stdout.write(f"Created: {name or 'Unnamed road'} ({source_id})")
            else:
                updated_count += 1
                self.stdout.write(f"Updated: {name or 'Unnamed road'} ({source_id})")

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully processed: {created_count} created, {updated_count} updated, {skipped_count} skipped"
            )
        )
