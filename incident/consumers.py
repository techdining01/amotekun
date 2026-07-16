import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from redis.exceptions import TimeoutError as RedisTimeoutError, ConnectionError as RedisConnectionError

_REDIS_ERRORS = (RedisTimeoutError, RedisConnectionError, OSError)


class NotificationConsumer(AsyncWebsocketConsumer):

    RECONNECT_DELAY = 3
    MAX_RECONNECT = 3
    PING_INTERVAL = 60  # seconds — increased to reduce traffic

    async def connect(self):
        if self.scope["user"].is_anonymous:
            await self.close()
            return

        self.user = self.scope["user"]
        self.user_group_name = f"user_{self.user.id}"
        self._group_joined = False
        self._ping_task = None

        await self.accept()

        # Check if channel layer is available (InMemory has no Redis dependency)
        from channels.layers import get_channel_layer
        layer = get_channel_layer()
        self._has_channel_layer = layer is not None

        if self._has_channel_layer:
            await self._join_group_with_retry()
        self._ping_task = asyncio.create_task(self._keepalive())

        count = await self.get_unread_count()
        await self._safe_send({"type": "unread_count", "count": count})

    async def disconnect(self, close_code):
        if self._ping_task and not self._ping_task.done():
            self._ping_task.cancel()
            try:
                await asyncio.wait_for(asyncio.shield(self._ping_task), timeout=1.0)
            except (asyncio.CancelledError, asyncio.TimeoutError):
                pass
        if self._group_joined and hasattr(self, "user_group_name"):
            try:
                await asyncio.wait_for(
                    self.channel_layer.group_discard(self.user_group_name, self.channel_name),
                    timeout=2.0,
                )
            except Exception:
                pass

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except (json.JSONDecodeError, TypeError):
            return

        t = data.get("type")
        if t == "mark_read":
            await self.mark_notification_read(data.get("notification_id"))
        elif t == "mark_all_read":
            await self.mark_all_notifications_read()
        elif t == "get_unread_count":
            count = await self.get_unread_count()
            await self._safe_send({"type": "unread_count", "count": count})
        elif t == "ping":
            await self._safe_send({"type": "pong"})
        elif t == "reconnect" and not self._group_joined:
            await self._join_group_with_retry()

    async def dispatch(self, message):
        try:
            await super().dispatch(message)
        except _REDIS_ERRORS:
            self._group_joined = False
            await self._safe_send({"type": "error", "message": "redis_timeout"})

    async def _join_group_with_retry(self):
        for attempt in range(self.MAX_RECONNECT):
            try:
                await self.channel_layer.group_add(self.user_group_name, self.channel_name)
                self._group_joined = True
                return
            except _REDIS_ERRORS:
                if attempt < self.MAX_RECONNECT - 1:
                    await asyncio.sleep(self.RECONNECT_DELAY)
        self._group_joined = False

    async def _keepalive(self):
        try:
            while True:
                await asyncio.sleep(self.PING_INTERVAL)
                if not self._group_joined:
                    await self._join_group_with_retry()
                await self._safe_send({"type": "ping"})
        except asyncio.CancelledError:
            pass
        except Exception:
            pass

    async def notification(self, event):
        await self._safe_send({"type": "notification", "notification": event["notification"]})

    async def notification_update(self, event):
        await self._safe_send({"type": "notification_update", "notification": event["notification"]})

    async def _safe_send(self, data):
        try:
            await self.send(text_data=json.dumps(data))
        except Exception:
            pass

    @database_sync_to_async
    def get_unread_count(self):
        from notifications.models import Notification
        return Notification.objects.filter(recipient=self.user, is_read=False).count()

    @database_sync_to_async
    def mark_notification_read(self, notification_id):
        from notifications.models import Notification
        try:
            n = Notification.objects.get(id=notification_id, recipient=self.user)
            n.mark_as_read()
            return True
        except Notification.DoesNotExist:
            return False

    @database_sync_to_async
    def mark_all_notifications_read(self):
        from notifications.models import Notification
        Notification.objects.filter(recipient=self.user, is_read=False).update(is_read=True)
