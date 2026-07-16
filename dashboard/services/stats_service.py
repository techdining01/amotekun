from django.utils import timezone
from datetime import timedelta

from accounts.models import User

from reports.models import (
    Incident,
    FloodZone,
)

from analytics.models import (
    Hotspot,
)

from chat.models import (
    ChatMessage,
    ChatRoom,
)

from patrol.models import PatrolTeam

from surveillance.models import Camera

from dispatch.models import Dispatch

from traffic.models import TrafficFlow


class StatisticsService:

    """
    Central statistics provider.

    Every dashboard gets its cards from here.

    Never query models directly inside dashboard views.
    """

    def __init__(self):

        self.today = timezone.now().date()

        self.last_7_days = timezone.now() - timedelta(days=7)

        self.last_30_days = timezone.now() - timedelta(days=30)


        # --------------------------------------------------
    # INCIDENTS
    # --------------------------------------------------

    def incident_statistics(self):

        qs = Incident.objects.all()

        return {

            "total": qs.count(),

            "today": qs.filter(
                created_at__date=self.today
            ).count(),

            "last_7_days": qs.filter(
                created_at__gte=self.last_7_days
            ).count(),

            "crime": qs.filter(
                report_type="crime"
            ).count(),

            "fire": qs.filter(
                report_type="fire"
            ).count(),

            "flood": qs.filter(
                report_type="flood"
            ).count(),

            "violence": qs.filter(
                report_type="violence"
            ).count(),

            "accident": qs.filter(
                report_type="accident"
            ).count(),

        }

        # --------------------------------------------------
    # USERS
    # --------------------------------------------------

    def user_statistics(self):

        qs = User.objects.filter(is_active=True)

        return {

            "total": qs.count(),

            "admins": qs.filter(role="PLATFORM_ADMIN").count(),

            "analysts": qs.filter(role="ANALYST").count(),

            "responders": qs.filter(role="RESPONDER").count(),

            "citizens": qs.filter(role="CITIZEN").count(),

        }


        # --------------------------------------------------
    # PATROLS
    # --------------------------------------------------

    def patrol_statistics(self):

        qs = PatrolTeam.objects.all()

        return {

            "total": qs.count(),

            "active": qs.filter(
                status="AVAILABLE"
            ).count(),

            "on_patrol": qs.filter(
                status="ON_PATROL"
            ).count(),

            "cancelled": qs.filter(
                status="CANCELLED"
            ).count(),

        }

        # --------------------------------------------------
    # DISPATCH
    # --------------------------------------------------

    def dispatch_statistics(self):

        qs = Dispatch.objects.all()

        return {

            "total": qs.count(),

            "pending": qs.filter(
                status="PENDING"
            ).count(),

            "assigned": qs.filter(
                status="ASSIGNED"
            ).count(),

            "completed": qs.filter(
                status="COMPLETED"
            ).count(),

        }

        # --------------------------------------------------
    # CAMERAS
    # --------------------------------------------------

    def surveillance_statistics(self):

        qs = Camera.objects.all()

        return {

            "total": qs.count(),

            "online": qs.filter(
                is_online=True
            ).count(),

            "offline": qs.filter(
                is_online=False
            ).count(),

        }

        # --------------------------------------------------
    # TRAFFIC
    # --------------------------------------------------

    def traffic_statistics(self):

        qs = TrafficFlow.objects.all()

        return {

            "roads": qs.count(),

            "heavy": qs.filter(
                congestion_level="HEAVY"
            ).count(),

            "moderate": qs.filter(
                congestion_level="MODERATE"
            ).count(),

            "free": qs.filter(
                congestion_level="FREE"
            ).count(),

        }

        # --------------------------------------------------
    # HOTSPOTS
    # --------------------------------------------------

    def hotspot_statistics(self):

        qs = Hotspot.objects.all()

        return {

            "total": qs.count(),

            "crime": qs.filter(
                hotspot_type="crime"
            ).count(),

            "traffic": qs.filter(
                hotspot_type="traffic"
            ).count(),

            "violence": qs.filter(
                hotspot_type="violence"
            ).count(),

        }

        # --------------------------------------------------
    # CHAT
    # --------------------------------------------------

    def chat_statistics(self):

        return {

            "rooms": ChatRoom.objects.count(),

            "messages": ChatMessage.objects.count(),

            "unread": ChatMessage.objects.filter(
                is_read=False
            ).count(),

        }

        # --------------------------------------------------
    # REPORTS
    # --------------------------------------------------

    def report_statistics(self):

        return {

            "flood_zones": FloodZone.objects.count(),
        }

    def admin(self):

        return {
            "total_incidents": Incident.objects.count(),
            "active_dispatches": Dispatch.objects.filter(status="ACTIVE").count(),
            "active_patrols": PatrolTeam.objects.filter(status="ON_PATROL").count(),
            "registered_users": User.objects.count(),
            "crime_reports": Incident.objects.filter(report_type="crime").count(),
            "fire_reports": Incident.objects.filter(report_type="fire").count(),
            "flood_reports": Incident.objects.filter(report_type="flood").count(),
            "traffic_reports": Incident.objects.filter(report_type="accident").count(),
            "hotspots": Hotspot.objects.count(),
            "chat": ChatMessage.objects.count(),
            "cameras_online": Camera.objects.filter(status="online").count(),
            "cameras_offline": Camera.objects.filter(status="offline").count(),
            "cameras_offline_locations": Camera.objects.filter(status="offline")
            .values_list("location", flat=True)
            .distinct(),
        }


    def analyst(self):

        return {

            "incidents": self.incident_statistics(),

            "hotspots": self.hotspot_statistics(),

            "traffic": self.traffic_statistics(),

        }

    def citizen(self):

        return {

            "incidents": {

                "today": self.incident_statistics()["today"]

            },

            "traffic": self.traffic_statistics(),

        }

    def responder(self):

        return {

            "dispatch": self.dispatch_statistics(),

            "patrols": self.patrol_statistics(),

            "chat": self.chat_statistics(),

        }

    def super_admin(self):

        return {

            **self.admin(),

            "platform": {

                "users": User.objects.count(),

                "incidents": Incident.objects.count(),

                "messages": ChatMessage.objects.count(),

                "hotspots": Hotspot.objects.count(),

                "cameras": Camera.objects.count(),

                "ai_services": 8,

            }

        }

    