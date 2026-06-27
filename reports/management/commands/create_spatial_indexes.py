from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Create GiST spatial indexes for geometry columns used in the project"

    def handle(self, *args, **kwargs):
        stmts = [
            "CREATE INDEX IF NOT EXISTS reports_lga_geom_gist ON reports_lga USING GIST (geometry);",
            "CREATE INDEX IF NOT EXISTS reports_state_geom_gist ON reports_state USING GIST (geometry);",
            "CREATE INDEX IF NOT EXISTS stations_policestation_loc_gist ON stations_policestation USING GIST (location);",
            "CREATE INDEX IF NOT EXISTS stations_amotekunstation_loc_gist ON stations_amotekunstation USING GIST (location);",
        ]

        with connection.cursor() as cur:
            for s in stmts:
                try:
                    cur.execute(s)
                    self.stdout.write(self.style.SUCCESS(f"OK: {s}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"FAILED: {s} -> {e}"))
