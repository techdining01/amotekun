from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification


class NotificationService:
    """Service for sending real-time notifications"""
    
    def __init__(self):
        self.channel_layer = get_channel_layer()
    
    def send_notification(self, user, notification_type, title, message, data=None):
        """
        Create and send a notification to a user
        
        Args:
            user: User instance to receive notification
            notification_type: Type of notification
            title: Notification title
            message: Notification message
            data: Optional additional data (dict)
        """
        # Create notification in database
        notification = Notification.create_notification(
            recipient=user,
            notification_type=notification_type,
            title=title,
            message=message,
            data=data
        )
        
        # Send via WebSocket
        self._send_to_user(user, {
            "type": "notification",
            "notification": {
                "id": notification.id,
                "notification_type": notification.notification_type,
                "title": notification.title,
                "message": notification.message,
                "data": notification.data,
                "is_read": notification.is_read,
                "created_at": notification.created_at.isoformat()
            }
        })
        
        return notification
    
    def send_to_role(self, role, notification_type, title, message, data=None):
        """
        Send notification to all users with a specific role
        
        Args:
            role: Role to send to (e.g., 'OFFICER', 'DISPATCHER')
            notification_type: Type of notification
            title: Notification title
            message: Notification message
            data: Optional additional data (dict)
        """
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        users = User.objects.filter(role=role)
        notifications = []
        
        for user in users:
            notification = self.send_notification(
                user=user,
                notification_type=notification_type,
                title=title,
                message=message,
                data=data
            )
            notifications.append(notification)
        
        return notifications
    
    def send_to_officers_nearby(self, lat, lon, radius_km, notification_type, title, message, data=None):
        """
        Send notification to officers near a location
        
        Args:
            lat: Latitude
            lon: Longitude
            radius_km: Search radius in kilometers
            notification_type: Type of notification
            title: Notification title
            message: Notification message
            data: Optional additional data (dict)
        """
        from django.contrib.auth import get_user_model
        from django.contrib.gis.geos import Point
        from django.contrib.gis.measure import D
        
        User = get_user_model()
        point = Point(lon, lat, srid=4326)
        
        # This would require officers to have location fields
        # For now, send to all officers
        return self.send_to_role('OFFICER', notification_type, title, message, data)
    
    def _send_to_user(self, user, data):
        """Send data to user's WebSocket channel"""
        group_name = f"user_{user.id}"
        
        async_to_sync(self.channel_layer.group_send)(
            group_name,
            {
                "type": "notification",
                **data
            }
        )


# Singleton instance
notification_service = NotificationService()
