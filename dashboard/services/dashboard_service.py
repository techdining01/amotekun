from reports.models import Incident
from .stats_service import StatisticsService
from .activity_service import ActivityService
from .notification_service import NotificationService
from .ai_service import AIService
from .map_service import MapDataService
from .responder_service import ResponderService


class DashboardService:
    """High-level facade used by dashboard views. Views only import this class."""

    def __init__(self, user):
        self.user = user
        self.statistics = StatisticsService()
        self.activity = ActivityService()
        self.notifications = NotificationService()
        self.ai = AIService()
        self.map = MapDataService()

    def admin(self):
        from dispatch.models import Dispatch
        from notifications.models import Notification
        from surveillance.models import Camera
        stats = self.statistics.admin()
        return {
            **stats,
            "role_display": "Administrator",
            "total_users": stats.get("registered_users", 0),
            "today_incidents": Incident.objects.filter(
                created_at__date=self.statistics.today
            ).count(),
            "total_facilities": 0,
            "system_health": "Healthy",
            "recent_incidents": Incident.objects.order_by("-created_at")[:10],
            "recent_dispatches": Dispatch.objects.order_by("-created_at")[:10],
            "cameras": Camera.objects.order_by("-created_at")[:6],
            "notifications": Notification.objects.filter(recipient=self.user).order_by("-created_at")[:20],
            "activity": self.activity.admin(),
            "ai": self.ai.dashboard_summary(),
            "map_layers": self.map.map_payload(),
        }

    def super_admin(self):
        stats = self.statistics.super_admin()
        platform = stats.get("platform") or {}
        return {
            "role_display": "Super Administrator",
            "platform": platform,
            "activity": self.activity.super_admin(),
            "notifications": self.notifications.super_admin(self.user),
            "ai": self.ai.national_summary(),
            "map_layers": self.map.map_payload(),
        }

    def analyst(self):
        stats = self.statistics.analyst()
        incidents = stats.get("incidents") or {}
        hotspots = stats.get("hotspots") or {}
        return {
            "role_display": "Security Analyst",
            "total_incidents": incidents.get("total", 0),
            "hotspots": hotspots.get("total", 0),
            "model_accuracy": "N/A",
            "risk_index": "N/A",
            "activity": self.activity.analyst(),
            "notifications": self.notifications.analyst(self.user),
            "ai": self.ai.dashboard_summary(),
            "map_layers": self.map.map_payload(),
        }

    def citizen(self):
        stats = self.statistics.citizen()
        return {
            **stats,
            "role_display": "Citizen",
            "my_reports": 0,
            "open_cases": 0,
            "resolved_cases": 0,
            "alerts": 0,
            "notifications": self.notifications.citizen(self.user),
            "map_layers": self.map.map_payload(),
            "ai": self.ai.dashboard_summary(),
        }

    def auditor(self):
        return {
            "role_display": "Auditor",
            "audit_logs": 0,
            "failed_logins": 0,
            "security_alerts": 0,
            "compliance_score": "100%",
            "notifications": self.notifications.admin(self.user),
            "ai": self.ai.dashboard_summary(),
            "map_layers": self.map.map_payload(),
        }

    def responder(self):
        return ResponderService(self.user).dashboard()
