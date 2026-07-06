import json
import csv
from pathlib import Path
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from stations.models import Hospital


class Command(BaseCommand):
    help = "Load Nigerian health facilities from CSV or GeoJSON into the database"

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default='static/data/nga_health_facilities.csv',
            help='Path to the health facilities CSV or GeoJSON file'
        )

    def handle(self, *args, **kwargs):
        filepath = Path(kwargs['file'])
        if not filepath.exists():
            self.stdout.write(
                self.style.ERROR(f"File not found: {filepath}")
            )
            return

        if filepath.suffix == '.csv':
            self._load_from_csv(filepath)
        elif filepath.suffix == '.geojson':
            self._load_from_geojson(filepath)
        else:
            self.stdout.write(
                self.style.ERROR(f"Unsupported file format: {filepath.suffix}")
            )

    def _load_from_geojson(self, filepath):
        self.stdout.write(f"Loading from GeoJSON: {filepath}")
        with open(filepath, encoding='utf-8') as f:
            data = json.load(f)

        created_count = 0
        updated_count = 0

        for feature in data.get("features", []):
            props = feature["properties"]
            geometry = feature["geometry"]

            # Extract data - let's see what props we have based on typical health facility data
            name = props.get("name", props.get("facility_name", "")).strip()
            lga = props.get("lga", props.get("lganame", "")).strip()
            state = props.get("state", props.get("statename", "")).strip()
            ward = props.get("ward", props.get("wardname", "")).strip()
            # Build address
            address_parts = []
            if ward:
                address_parts.append(ward)
            if lga:
                address_parts.append(lga)
            if state:
                address_parts.append(state)
            address = ", ".join(address_parts).strip()

            # Extract new fields
            category = props.get("Category", props.get("category", "")).strip()
            ownership = props.get("Facility Ownership", props.get("ownership", "")).strip()
            function_type = props.get("Facility Type", props.get("function_type", "")).strip()
            function = props.get("function", props.get("description", "")).strip()
            status = props.get("Status", props.get("status", "")).strip()

            # Check if it's an emergency facility (we can default to True, or try to infer from props)
            has_emergency = props.get("has_emergency", False)
            if isinstance(has_emergency, str):
                has_emergency = has_emergency.lower() in ("true", "yes", "1", "y")
            # Also infer from category/facility type
            if any(keyword in category.lower() for keyword in ["emergency", "military", "hospital", "medical center"]):
                has_emergency = True
            if any(keyword in function_type.lower() for keyword in ["secondary", "tertiary", "hospital"]):
                has_emergency = True

            # Create point geometry
            location = None
            if geometry:
                if geometry.get("type") == "Point" and geometry.get("coordinates"):
                    lon, lat = geometry["coordinates"]
                    location = Point(lon, lat, srid=4326)
                elif geometry.get("type") in ["Polygon", "MultiPolygon"]:
                    # Calculate centroid if it's an area geometry
                    from django.contrib.gis.geos import GEOSGeometry
                    geom = GEOSGeometry(str(geometry), srid=4326)
                    location = geom.centroid

            # Get or create hospital
            if name:
                hospital, created = Hospital.objects.get_or_create(
                    name=name,
                    defaults={
                        'address': address,
                        'state': state,
                        'lga': lga,
                        'location': location,
                        'has_emergency': has_emergency,
                        'category': category,
                        'ownership': ownership,
                        'function_type': function_type,
                        'function': function,
                        'status': status
                    }
                )

                if created:
                    created_count += 1
                    self.stdout.write(f"Created: {name}")
                else:
                    # Update existing hospital
                    hospital.address = address
                    hospital.state = state
                    hospital.lga = lga
                    hospital.location = location
                    hospital.has_emergency = has_emergency
                    hospital.category = category
                    hospital.ownership = ownership
                    hospital.function_type = function_type
                    hospital.function = function
                    hospital.status = status
                    hospital.save()
                    updated_count += 1
                    self.stdout.write(f"Updated: {name}")

        self.stdout.write(
            self.style.SUCCESS(f"Successfully processed {created_count} created, {updated_count} updated health facilities")
        )

    def _load_from_csv(self, filepath):
        self.stdout.write(f"Loading from CSV: {filepath}")
        created_count = 0
        updated_count = 0

        with open(filepath, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row.get("Facility_name", "").strip()
                lga = row.get("LGA", "").strip()
                state = row.get("State", "").strip()
                ward = row.get("Ward", "").strip()

                # Build address
                address_parts = []
                if ward:
                    address_parts.append(ward)
                if lga:
                    address_parts.append(lga)
                if state:
                    address_parts.append(state)
                address = ", ".join(address_parts).strip()

                # Extract new fields from CSV
                category = row.get("Category", "").strip()
                ownership = row.get("Facility Ownership", "").strip()
                function_type = row.get("Facility Type", "").strip()
                status = row.get("Status", "").strip()
                function = ""  # Not available in CSV, but we'll leave it empty

                # Parse coordinates
                location = None
                try:
                    lat = float(row.get("Latitude", 0))
                    lon = float(row.get("Longitude", 0))
                    if lat != 0 and lon != 0:
                        location = Point(lon, lat, srid=4326)
                except (ValueError, TypeError):
                    pass

                # Check if it's an emergency facility
                # Consider secondary/tertiary facilities, military, etc. as having emergency
                has_emergency = False
                if any(keyword in category.lower() for keyword in ["emergency", "military", "hospital", "medical center"]):
                    has_emergency = True
                if any(keyword in function_type.lower() for keyword in ["secondary", "tertiary", "hospital"]):
                    has_emergency = True

                # Get or create hospital
                if name:
                    hospital, created = Hospital.objects.get_or_create(
                        name=name,
                        defaults={
                            'address': address,
                            'state': state,
                            'lga': lga,
                            'location': location,
                            'has_emergency': has_emergency,
                            'category': category,
                            'ownership': ownership,
                            'function_type': function_type,
                            'function': function,
                            'status': status
                        }
                    )

                    if created:
                        created_count += 1
                        self.stdout.write(f"Created: {name}")
                    else:
                        # Update existing hospital
                        hospital.address = address
                        hospital.state = state
                        hospital.lga = lga
                        hospital.location = location
                        hospital.has_emergency = has_emergency
                        hospital.category = category
                        hospital.ownership = ownership
                        hospital.function_type = function_type
                        hospital.function = function
                        hospital.status = status
                        hospital.save()
                        updated_count += 1
                        self.stdout.write(f"Updated: {name}")

        self.stdout.write(
            self.style.SUCCESS(f"Successfully processed {created_count} created, {updated_count} updated health facilities")
        )
