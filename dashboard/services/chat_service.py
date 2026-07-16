from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

from chat.models import ChatRoom, ChatMessage


class ChatService:

    @staticmethod
    def summary():
        return {
            "total_rooms": ChatRoom.objects.count(),
            "total_messages": ChatMessage.objects.count(),
            "unread_messages": ChatMessage.objects.filter(is_read=False).count(),
            "active_today": ChatMessage.objects.filter(
                created_at__date=timezone.now().date()
            ).count(),
        }

    @staticmethod
    def recent_messages(limit=20):
        return (
            ChatMessage.objects.select_related("sender", "room")
            .order_by("-created_at")[:limit]
        )

    @staticmethod
    def rooms_with_unread():
        return (
            ChatRoom.objects.annotate(
                unread_count=Count("messages", filter=Q(messages__is_read=False))
            )
            .filter(unread_count__gt=0)
            .order_by("-unread_count")
        )

    @staticmethod
    def unread_for_user(user):
        return ChatMessage.objects.filter(
            is_read=False,
            room__in=ChatRoom.objects.filter(messages__sender=user),
        ).exclude(sender=user).count()

    @staticmethod
    def rooms_for_incident(incident):
        return ChatRoom.objects.filter(incident=incident).prefetch_related("messages")

    @staticmethod
    def rooms_for_dispatch(dispatch):
        return ChatRoom.objects.filter(dispatch=dispatch).prefetch_related("messages")

    @staticmethod
    def activity_last_hours(hours=24):
        since = timezone.now() - timedelta(hours=hours)
        return (
            ChatMessage.objects.filter(created_at__gte=since)
            .values("room__name", "room__room_type")
            .annotate(message_count=Count("id"))
            .order_by("-message_count")
        )
