from django.utils import timezone
from datetime import timedelta

from reports.models import Incident
from dispatch.models import Dispatch
from patrol.models import PatrolTeam
from chat.models import ChatMessage
from analytics.models import HotspotAnalysis

# from surveillance.models import Detection
from traffic.models import TrafficFlow, TrafficAlert



class ActivityService:

    """
    Provides live activities shown across dashboards.

    Timeline
    Recent cards
    Live feed
    Recent widgets

    Dashboard never queries models directly.
    """

    def __init__(self):

        self.now = timezone.now()

        self.today = self.now.date()

        self.last_24_hours = self.now - timedelta(hours=24)

    
    def recent_incidents(self, limit=10):

        return (
            Incident.objects
            .select_related("reporter")
            .order_by("-created_at")[:limit]
        )

    def recent_dispatches(self, limit=10):

        return (
            Dispatch.objects
            .select_related("reporter")
            .order_by("-created_at")[:limit]
        )

    def recent_patrols(self, limit=10):

        return (
            PatrolTeam.objects
            .select_related("agency")
            .order_by("-created_at")[:limit]
        )

    def recent_messages(self, limit=10):

        return (
            ChatMessage.objects
            .select_related("reporter")
            .order_by("-created_at")[:limit]
        )

    def recent_hotspots(self, limit=10):

        return (
            HotspotAnalysis.objects
            .select_related("reporter")
            .order_by("-created_at")[:limit]
        )

    def recent_camera_detections(self, limit=10):

        return (
            TrafficAlert.objects
            .select_related("reporter")
            .order_by("-created_at")[:limit]
        )

    def recent_traffic(self, limit=10):

        return (
            TrafficFlow.objects
            .select_related("reporter")
            .order_by("-measured_at")[:limit]
        )

    def recent_hotspot_analysis(self, limit=10):

        return (
            HotspotAnalysis.objects
            .select_related("reporter")
            .order_by("-created_at")[:limit]
        )

    def dashboard_feed(self):

        return {

            "incidents": self.recent_incidents(5),

            "dispatches": self.recent_dispatches(5),

            "patrols": self.recent_patrols(5),

            "messages": self.recent_messages(5),

            "detections": self.recent_camera_detections(5),

            "traffic": self.recent_traffic(5),

            "analytics": self.recent_hotspot_analysis(5),

        }

    def admin(self):

        return (

            Incident.objects

            .select_related("reporter")

            .order_by("-created_at")[:20]

        )

    def super_admin(self):

        return self.dashboard_feed()

    def analyst(self):

        return {

            "incidents": self.recent_incidents(),

            "traffic": self.recent_traffic(),

            "analytics": self.recent_hotspot_analysis(),

        }

    def citizen(self):

        return {

            "incidents": self.recent_incidents(6),

            "traffic": self.recent_traffic(6),

        }

    def responder(self):

        return {

            "dispatches": self.recent_dispatches(),

            "patrols": self.recent_patrols(),

            "messages": self.recent_messages(),

            "detections": self.recent_camera_detections(),

        }       

    