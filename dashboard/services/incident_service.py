from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

from reports.models import Incident, IncidentHistory


class IncidentService:

    @staticmethod
    def summary():
        qs = Incident.objects.all()
        today = timezone.now().date()
        last_7 = timezone.now() - timedelta(days=7)

        return {
            "total": qs.count(),
            "today": qs.filter(created_at__date=today).count(),
            "last_7_days": qs.filter(created_at__gte=last_7).count(),
            "by_status": {
                "pending": qs.filter(status="pending").count(),
                "verified": qs.filter(status="verified").count(),
                "dispatched": qs.filter(status="dispatched").count(),
                "resolved": qs.filter(status="resolved").count(),
                "closed": qs.filter(status="closed").count(),
            },
            "by_priority": {
                "critical": qs.filter(priority="critical").count(),
                "high": qs.filter(priority="high").count(),
                "medium": qs.filter(priority="medium").count(),
                "low": qs.filter(priority="low").count(),
            },
            "by_type": {
                "crime": qs.filter(report_type="crime").count(),
                "violence": qs.filter(report_type="violence").count(),
                "fire": qs.filter(report_type="fire").count(),
                "flood": qs.filter(report_type="flood").count(),
                "accident": qs.filter(report_type="accident").count(),
            },
        }

    @staticmethod
    def recent(limit=10):
        return (
            Incident.objects.select_related("reporter", "assigned_team", "dispatcher")
            .order_by("-created_at")[:limit]
        )

    @staticmethod
    def pending():
        return Incident.objects.filter(status="pending").order_by("-created_at")

    @staticmethod
    def critical():
        return Incident.objects.filter(
            priority="critical", status__in=["pending", "verified", "dispatched"]
        ).order_by("-created_at")

    @staticmethod
    def by_state():
        return (
            Incident.objects.values("state")
            .annotate(count=Count("id"))
            .order_by("-count")
        )

    @staticmethod
    def by_lga():
        return (
            Incident.objects.values("lga", "state")
            .annotate(count=Count("id"))
            .order_by("-count")
        )

    @staticmethod
    def trend(days=30):
        since = timezone.now() - timedelta(days=days)
        return (
            Incident.objects.filter(created_at__gte=since)
            .values("created_at__date", "report_type")
            .annotate(count=Count("id"))
            .order_by("created_at__date")
        )

    @staticmethod
    def for_user(user):
        return Incident.objects.filter(reporter=user).order_by("-created_at")

    @staticmethod
    def history(incident):
        return IncidentHistory.objects.filter(incident=incident).select_related("user")
