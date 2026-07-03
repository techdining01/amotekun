from django.core.management.base import BaseCommand
from traffic.services import TrafficCollectionService


class Command(BaseCommand):
    help = "Collect traffic snapshots from the configured traffic provider."

    def add_arguments(self, parser):
        parser.add_argument(
            "--provider",
            type=str,
            default="tomtom",
            help="Traffic provider name to use for collection.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Run collection without saving snapshots.",
        )

    def handle(self, *args, **options):
        provider_name = options["provider"]
        dry_run = options["dry_run"]

        self.stdout.write(
            self.style.NOTICE(f"Starting traffic collection: {provider_name}")
        )

        service = TrafficCollectionService(provider_name=provider_name)
        snapshots = service.collect(dry_run=dry_run)

        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f"Dry run complete. {len(snapshots)} snapshots prepared."
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f"Saved {len(snapshots)} traffic snapshots.")
            )

        self.stdout.write(self.style.SUCCESS("Traffic collection complete."))
