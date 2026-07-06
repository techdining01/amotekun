from django.core.management.base import BaseCommand
from django.db import connection
from psycopg2 import sql


class Command(BaseCommand):
    help = "Prepare a roads_edges table for pgRouting from the reports_road table"

    def add_arguments(self, parser):
        parser.add_argument(
            "--tolerance",
            type=float,
            default=0.0001,
            help="Topology snapping tolerance",
        )
        parser.add_argument(
            "--table", default="reports_road", help="Source roads table name"
        )
        parser.add_argument(
            "--geom", default="geometry", help="Geometry column name on source table"
        )

    def handle(self, *args, **options):
        table = options["table"]
        geom = options["geom"]
        tol = options["tolerance"]

        with connection.cursor() as cur:
            # verify source table exists
            cur.execute("SELECT to_regclass(%s)", [table])
            reg = cur.fetchone()
            if not reg or not reg[0]:
                self.stdout.write(
                    self.style.ERROR(f"Source table {table} not found")
                )
                return

            # check pgrouting installed
            cur.execute("SELECT extname FROM pg_extension WHERE extname='pgrouting'")
            if not cur.fetchone():
                self.stdout.write(
                    self.style.ERROR(
                        "pgRouting extension not found in DB. Install it before running this command."
                    )
                )
                return

            # check for missing source/target columns
            cur.execute(
                "SELECT column_name FROM information_schema.columns WHERE table_name=%s AND column_name IN ('source','target')",
                [table],
            )
            cols = [r[0] for r in cur.fetchall()]
            
            if "source" not in cols or "target" not in cols:
                try:
                    # Manually inject the target/source columns first to ensure data-type integrity
                    self.stdout.write(f"Preparing routing columns on {table}...")
                    cur.execute(
                        sql.SQL(
                            "ALTER TABLE {} "
                            "ADD COLUMN IF NOT EXISTS source INTEGER, "
                            "ADD COLUMN IF NOT EXISTS target INTEGER;"
                        ).format(sql.Identifier(table))
                    )

                    self.stdout.write(
                        f"Running pgr_createTopology on {table} (tolerance={tol})..."
                    )
                    cur.execute(
                        "SELECT public.pgr_createTopology(%s::text, %s::float8, %s::text, %s::text);",
                        [table, tol, geom, "id"],
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"pgr_createTopology failed: {e}")
                    )
                    return
            else:
                self.stdout.write(
                    "Table already has source/target columns; skipping pgr_createTopology."
                )

            # create roads_edges table from the table with cost = length in meters (transform to 3857)
            try:
                cur.execute(sql.SQL("DROP TABLE IF EXISTS public.{} CASCADE;").format(
                    sql.Identifier("roads_edges")
                ))
                
                # FIX: Removed ::geography cast. ST_Transform requires geometry type directly.
                cur.execute(
                    sql.SQL(
                        "CREATE TABLE public.roads_edges AS SELECT id, source, target, "
                        "ST_Length(ST_Transform({}::geometry, 3857)) AS cost, "
                        "ST_Length(ST_Transform({}::geometry, 3857)) AS reverse_cost "
                        "FROM public.{};"
                    ).format(sql.Identifier(geom), sql.Identifier(geom), sql.Identifier(table))
                )
                cur.execute("ALTER TABLE public.roads_edges ADD PRIMARY KEY (id);")
                cur.execute(
                    "CREATE INDEX IF NOT EXISTS roads_edges_source_idx ON public.roads_edges (source);"
                )
                cur.execute(
                    "CREATE INDEX IF NOT EXISTS roads_edges_target_idx ON public.roads_edges (target);"
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        "Created public.roads_edges with cost computed as length (meters)."
                    )
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Failed to create roads_edges: {e}")
                )
