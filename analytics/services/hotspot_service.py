from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.utils import timezone
from reports.models import Incident
from analytics.models import Hotspot, HotspotAnalysis


class HotspotService:

    def compute_hotspots(self, hotspot_type: str = "crime", radius_km: float = 1.0, min_incidents: int = 2):
        """
        Cluster incidents by proximity and create Hotspot records.
        Returns list of created Hotspot instances.
        """
        type_map = {
            "crime": ["crime", "violence"],
            "violence": ["violence"],
            "traffic": ["accident"],
        }
        report_types = type_map.get(hotspot_type, [hotspot_type])
        incidents = Incident.objects.filter(report_type__in=report_types)

        visited = set()
        hotspots = []

        for incident in incidents:
            if incident.pk in visited:
                continue

            nearby = Incident.objects.filter(
                report_type__in=report_types,
                geometry__distance_lte=(incident.geometry, D(km=radius_km)),
            )
            count = nearby.count()

            if count < min_incidents:
                continue

            for n in nearby:
                visited.add(n.pk)

            intensity = min(1.0, count / 20.0)

            hotspot = Hotspot.objects.create(
                location=incident.geometry,
                hotspot_type=hotspot_type,
                intensity_score=intensity,
                incident_count=count,
            )
            hotspots.append(hotspot)

        return hotspots

    def run_analysis(self, hotspot_type: str = "crime", radius_km: float = 1.0):
        analysis = HotspotAnalysis.objects.create(
            analysis_type=f"{hotspot_type}_clustering",
            parameters={"radius_km": radius_km, "hotspot_type": hotspot_type},
        )
        hotspots = self.compute_hotspots(hotspot_type=hotspot_type, radius_km=radius_km)
        analysis.results = {
            "hotspot_count": len(hotspots),
            "hotspot_ids": [h.pk for h in hotspots],
        }
        analysis.completed_at = timezone.now()
        analysis.save(update_fields=["results", "completed_at"])
        return analysis

    def get_hotspots(self, hotspot_type: str = None, lat: float = None, lon: float = None, radius_km: float = 10.0):
        qs = Hotspot.objects.all()
        if hotspot_type:
            qs = qs.filter(hotspot_type=hotspot_type)
        if lat is not None and lon is not None:
            point = Point(lon, lat, srid=4326)
            qs = qs.filter(location__distance_lte=(point, D(km=radius_km)))
        return qs

