from itertools import chain
from django.shortcuts import render
from django.utils import timezone
from reports.models import Incident
from dispatch.models import Dispatch
from chat.models import ChatMessage
from analytics.models import Hotspot
from surveillance.models import CameraAlert

class NotificationService:

    """
    Unified notification provider.
    Dashboard never queries apps directly.
    Every notification returned here has the same structure.
    """

    def incident_notifications(self, limit=10):

        notifications = []

        incidents = (
            Incident.objects
            .order_by("-created_at")[:limit]
        )

        for incident in incidents:

            notifications.append({

                "type": "incident",

                "title": incident.title or "",

                "message": (incident.description or "")[:70],

                "time": incident.created_at,

                "icon": "triangle-alert",

                "color": "red",

                "url": f"/reports/{incident.pk}/",

            })

        return notifications

    def dispatch_notifications(self, limit=10):

        items = []

        dispatches = (
            Dispatch.objects
            .order_by("-created_at")[:limit]
        )

        for dispatch in dispatches:

            items.append({

                "type": "dispatch",

                "title": "Dispatch Created",

                "message": str(dispatch),

                "time": dispatch.created_at,

                "icon": "truck",

                "color": "blue",

                "url": f"/dispatch/{dispatch.pk}/",

            })

        return items


    def chat_notifications(self, limit=10):

        items = []

        messages = (
            ChatMessage.objects
            .select_related("room")
            .order_by("-created_at")[:limit]
        )

        for message in messages:

            items.append({

                "type": "chat",

                "title": "New Message",

                "message": (message.content or "")[:70],

                "time": message.created_at,

                "icon": "message-square",

                "color": "green",

                "url": f"/chat/{message.room_id}/",

            })

        return items

    def hotspot_notifications(self, limit=5):

        items = []

        hotspots = (

            Hotspot.objects

            .order_by("-calculated_at")[:limit]

        )

        for hotspot in hotspots:

            items.append({

                "type": "hotspot",

                "title": "AI Hotspot",

                "message": hotspot.hotspot_type,

                "time": hotspot.calculated_at,

                "icon": "brain",

                "color": "purple",

                "url": "/analytics/hotspots/",

            })

        return items

    def camera_notifications(self, limit=10):

        items = []

        alerts = (

            CameraAlert.objects

            .select_related("camera")

            .order_by("-created_at")[:limit]

        )

        for alert in alerts:

            items.append(
                {
                    "type": "camera",
                    "title": alert.camera.name,
                    "message": alert.message,
                    "time": alert.created_at,
                    "icon": "camera",
                    "color": "emerald",
                    "url": f"/surveillance/cameras/{alert.camera_id}/",
                }
            )

        return items


    def traffic_notifications(self, limit=10):
        items = []
        from traffic.models import TrafficFlow
        flows = TrafficFlow.objects.select_related("road").order_by("-measured_at")[:limit]
        for flow in flows:
            items.append({
                "type": "traffic",
                "title": flow.road.name if flow.road else "Road",
                "message": flow.congestion_level,
                "time": flow.measured_at,
                "icon": "car",
                "color": "orange",
                "url": "/traffic/",
            })
        return items

    def all_notifications(self, user):

        notifications = list(

            chain(

                self.incident_notifications(),

                self.dispatch_notifications(),

                self.chat_notifications(),

                self.camera_notifications(),

                self.hotspot_notifications(),

                self.traffic_notifications(),

            )

        )

        notifications.sort(

            key=lambda x: x["time"] or timezone.now(),

            reverse=True,

        )

        return notifications

    def unread_count(self, user):

        return len(self.all_notifications(user))

    


    def admin(self, user):

        return Incident.objects.order_by(

            "-created_at"

        )[:10]

    def super_admin(self, user):

        return self.all_notifications(user)

    def analyst(self, user=None):

        notifications = list(

            chain(

                self.incident_notifications(),

                self.hotspot_notifications(),

                self.traffic_notifications(),

            )

        )

        notifications.sort(

            key=lambda x: x["time"] or timezone.now(),

            reverse=True,

        )

        return notifications

    def citizen(self, user=None):

        return self.incident_notifications(5)

    def responder(self, user):

        notifications = list(

            chain(

                self.dispatch_notifications(),

                self.chat_notifications(),

                self.camera_notifications(),

            )

        )

        notifications.sort(

            key=lambda x: x["time"] or timezone.now(),

            reverse=True,

        )

        return notifications

    def notification_list(request):

        notifications = NotificationService().admin(request.user)

        return render(

            request,

            "dashboard/widgets/notifications.html",

            {

                "notifications": notifications,

            },

        )