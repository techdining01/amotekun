import json

from django.core.management.base import BaseCommand
from django.db import connection

from reports.models import Ward, LGA


class Command(BaseCommand):
    help = "Load Nigerian ward boundaries from GeoJSON into PostGIS"

    def handle(self, *args, **kwargs):
        filepath = "static/data/NGA_Ward_Boundaries.geojson"

        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)

        cursor = connection.cursor()
        created_count = 0
        updated_count = 0

        for feature in data["features"]:
            props = feature["properties"]
            geometry = feature["geometry"]

            ward_name = props.get("wardname", "").strip()
            lga_name = props.get("lganame", "").strip()

            if not ward_name or not lga_name:
                continue

            if geometry is None:
                continue

            # Get or create LGA (only set name, geometry can be null)
            cursor.execute("SELECT id FROM reports_lga WHERE name = %s", [lga_name])
            lga_row = cursor.fetchone()
            if lga_row:
                lga_id = lga_row[0]
            else:
                cursor.execute(
                    "INSERT INTO reports_lga (name) VALUES (%s)",
                    [lga_name]
                )
                cursor.execute("SELECT id FROM reports_lga WHERE name = %s", [lga_name])
                lga_id = cursor.fetchone()[0]

            # Check if ward exists
            cursor.execute(
                "SELECT id FROM reports_ward WHERE lga_id = %s AND name = %s",
                [lga_id, ward_name]
            )
            existing = cursor.fetchone()

            if existing:
                cursor.execute(
                    "UPDATE reports_ward SET geometry = ST_GeomFromGeoJSON(%s), is_active = TRUE, updated_at = NOW() WHERE id = %s",
                    [json.dumps(geometry), existing[0]]
                )
                updated_count += 1
            else:
                cursor.execute(
                    "INSERT INTO reports_ward (lga_id, name, geometry, is_active, created_at, updated_at) VALUES (%s, %s, ST_GeomFromGeoJSON(%s), TRUE, NOW(), NOW())",
                    [lga_id, ward_name, json.dumps(geometry)]
                )
                created_count += 1

        cursor.close()

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully processed wards — created: {created_count}, updated: {updated_count}"
            )
        )