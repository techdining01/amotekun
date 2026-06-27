from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Validate SRIDs and run ST_MakeValid on common geometry columns"

    def handle(self, *args, **kwargs):
        # This command is conservative: it only ALTERs geometries when SRID mismatch or invalid geometries found.
        checks = [
            ("reports_lga", "geometry"),
            ("reports_state", "geometry"),
            ("stations_policestation", "location"),
            ("stations_amotekunstation", "location"),
        ]

        with connection.cursor() as cur:
            for table, col in checks:
                try:
                    # set SRID if null
                    cur.execute(
                        f"UPDATE {table} SET {col} = ST_SetSRID({col},4326) WHERE ST_SRID({col}) IS NULL;"
                    )
                    # make valid where needed
                    cur.execute(
                        f"UPDATE {table} SET {col} = ST_MakeValid({col}) WHERE NOT ST_IsValid({col});"
                    )
                    self.stdout.write(self.style.SUCCESS(f"Validated {table}.{col}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Failed {table}.{col} -> {e}"))
