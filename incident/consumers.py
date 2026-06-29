import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

User = get_user_model()


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Handle WebSocket connection"""
        if self.scope["user"].is_anonymous:
            await self.close()
            return
        
        self.user = self.scope["user"]
        self.user_group_name = f"user_{self.user.id}"
        
        # Join user's personal notification group
        await self.channel_layer.group_add(
            self.user_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Send unread count on connect
        unread_count = await self.get_unread_count()
        await self.send(text_data=json.dumps({
            "type": "unread_count",
            "count": unread_count
        }))
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection"""
        # Leave user's notification group
        await self.channel_layer.group_discard(
            self.user_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        """Handle incoming WebSocket messages"""
        try:
            data = json.loads(text_data)
            message_type = data.get("type")
            
            if message_type == "mark_read":
                notification_id = data.get("notification_id")
                await self.mark_notification_read(notification_id)
            elif message_type == "mark_all_read":
                await self.mark_all_notifications_read()
            elif message_type == "get_unread_count":
                unread_count = await self.get_unread_count()
                await self.send(text_data=json.dumps({
                    "type": "unread_count",
                    "count": unread_count
                }))
        except json.JSONDecodeError:
            pass
    
    async def notification(self, event):
        """Handle notification event from channel layer"""
        # Send notification to WebSocket
        await self.send(text_data=json.dumps({
            "type": "notification",
            "notification": event["notification"]
        }))
    
    async def notification_update(self, event):
        """Handle notification update event"""
        await self.send(text_data=json.dumps({
            "type": "notification_update",
            "notification": event["notification"]
        }))
    
    @database_sync_to_async
    def get_unread_count(self):
        """Get unread notification count"""
        from notifications.models import Notification
        return Notification.objects.filter(
            recipient=self.user,
            is_read=False
        ).count()
    
    @database_sync_to_async
    def mark_notification_read(self, notification_id):
        """Mark a specific notification as read"""
        from notifications.models import Notification
        try:
            notification = Notification.objects.get(
                id=notification_id,
                recipient=self.user
            )
            notification.mark_as_read()
            return True
        except Notification.DoesNotExist:
            return False
    
    @database_sync_to_async
    def mark_all_notifications_read(self):
        """Mark all notifications as read"""
        from notifications.models import Notification
        Notification.objects.filter(
            recipient=self.user,
            is_read=False
        ).update(is_read=True)
