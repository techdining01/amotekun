from django.utils import timezone
from reports.models import Incident
from dispatch.models import Dispatch
from patrol.models import PatrolTeam, PatrolMission
from chat.models import ChatRoom, ChatMessage
from surveillance.models import Camera, CameraAlert
from analytics.models import Hotspot
from traffic.models import TrafficFlow


class ResponderService:
    def __init__(self, user):
        self.user = user
        self.today = timezone.now().date()
        self.now = timezone.now()

    def current_dispatch(self):
        # Dispatch is linked to patrol_team; find via accepted_by or dispatcher
        return (
            Dispatch.objects
            .select_related("incident")
            .filter(accepted_by=self.user, status__in=["accepted", "in_progress", "dispatched"])
            .order_by("-created_at")
            .first()
        )

    def dispatch_history(self, limit=20):
        return (
            Dispatch.objects
            .select_related("incident")
            .filter(accepted_by=self.user)
            .order_by("-created_at")[:limit]
        )

    def current_patrol_team(self):
        return (
            PatrolTeam.objects
            .filter(commander=self.user, status="ON_PATROL")
            .first()
        )

    def my_incidents(self):
        dispatch = self.current_dispatch()
        if not dispatch:
            return Incident.objects.none()
        return Incident.objects.filter(pk=dispatch.incident_id)

    def nearby_hotspots(self):
        return Hotspot.objects.order_by("-intensity_score")[:10]

    def nearby_traffic(self):
        return TrafficFlow.objects.order_by("-measured_at")[:10]

    def chat_rooms(self):
        return ChatRoom.objects.filter(messages__sender=self.user).distinct()

    def recent_messages(self):
        return (
            ChatMessage.objects
            .filter(room__in=self.chat_rooms())
            .exclude(sender=self.user)
            .order_by("-created_at")[:20]
        )

    def unread_message_count(self):
        return (
            ChatMessage.objects
            .filter(room__in=self.chat_rooms(), is_read=False)
            .exclude(sender=self.user)
            .count()
        )

    def nearby_camera_alerts(self):
        return CameraAlert.objects.select_related("camera").order_by("-created_at")[:10]

    def nearby_cameras(self):
        return Camera.objects.filter(status="online").order_by("name")[:20]

    def today_statistics(self):
        return {
            "dispatches": Dispatch.objects.filter(
                accepted_by=self.user, created_at__date=self.today
            ).count(),
            "patrol_teams": PatrolTeam.objects.filter(
                commander=self.user, created_at__date=self.today
            ).count(),
            "messages": self.unread_message_count(),
            "camera_alerts": CameraAlert.objects.filter(
                created_at__date=self.today
            ).count(),
        }

    def dashboard(self):
        dispatch = self.current_dispatch()
        return {
            "role_display": "Responder",
            "assigned_incidents": Dispatch.objects.filter(
                accepted_by=self.user, status__in=["accepted", "in_progress"]
            ).count(),
            "resolved_today": Dispatch.objects.filter(
                accepted_by=self.user, status="resolved", resolved_at__date=self.today
            ).count(),
            "distance_remaining": "N/A",
            "eta": "N/A",
            "dispatches": self.dispatch_history(10),
            "statistics": self.today_statistics(),
            "dispatch": dispatch,
            "patrol_team": self.current_patrol_team(),
            "incidents": self.my_incidents(),
            "traffic": self.nearby_traffic(),
            "hotspots": self.nearby_hotspots(),
            "messages": self.recent_messages(),
            "camera_alerts": self.nearby_camera_alerts(),
            "cameras": self.nearby_cameras(),
        }
