from django.db.models import Count, Avg, Max
from django.utils import timezone
from datetime import timedelta

from analytics.models import Hotspot, HotspotAnalysis


class AnalyticsService:

    @staticmethod
    def summary():
        qs = Hotspot.objects.all()
        return {
            "total_hotspots": qs.count(),
            "crime": qs.filter(hotspot_type="crime").count(),
            "violence": qs.filter(hotspot_type="violence").count(),
            "traffic": qs.filter(hotspot_type="traffic").count(),
            "avg_intensity": qs.aggregate(avg=Avg("intensity_score"))["avg"] or 0,
            "high_intensity": qs.filter(intensity_score__gte=0.7).count(),
        }

    @staticmethod
    def top_hotspots(hotspot_type=None, limit=10):
        qs = Hotspot.objects.all()
        if hotspot_type:
            qs = qs.filter(hotspot_type=hotspot_type)
        return qs.order_by("-intensity_score")[:limit]

    @staticmethod
    def recent_analyses(limit=5):
        return HotspotAnalysis.objects.order_by("-created_at")[:limit]

    @staticmethod
    def hotspot_trend(days=7):
        since = timezone.now() - timedelta(days=days)
        return (
            Hotspot.objects.filter(calculated_at__gte=since)
            .values("calculated_at__date", "hotspot_type")
            .annotate(count=Count("id"), avg_intensity=Avg("intensity_score"))
            .order_by("calculated_at__date")
        )

    @staticmethod
    def incident_hotspot_correlation():
        from reports.models import Incident
        from django.contrib.gis.measure import D

        hotspots = Hotspot.objects.filter(intensity_score__gte=0.5)
        results = []
        for hotspot in hotspots:
            nearby = Incident.objects.filter(
                geometry__distance_lte=(hotspot.location, D(km=2))
            ).count()
            results.append({
                "hotspot_id": hotspot.id,
                "hotspot_type": hotspot.hotspot_type,
                "intensity": hotspot.intensity_score,
                "nearby_incidents": nearby,
            })
        return sorted(results, key=lambda x: -x["nearby_incidents"])
