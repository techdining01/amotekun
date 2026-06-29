from django.db import models
from django.conf import settings


class ChatRoom(models.Model):
    """Chat room for operative communication"""
    ROOM_TYPES = [
        ('general', 'General'),
        ('incident', 'Incident Specific'),
        ('dispatch', 'Dispatch Team'),
        ('station', 'Station'),
    ]
    
    name = models.CharField(max_length=200)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES, default='general')
    incident = models.ForeignKey(
        'reports.Incident',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='chat_rooms'
    )
    dispatch = models.ForeignKey(
        'dispatch.Dispatch',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='chat_rooms'
    )
    station = models.ForeignKey(
        'stations.PoliceStation',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='chat_rooms'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.room_type})"
    
    def get_participants(self):
        """Get all users who have sent messages in this room"""
        user_ids = self.messages.values_list('sender', flat=True).distinct()
        return settings.AUTH_USER_MODEL.objects.filter(id__in=user_ids)


class ChatMessage(models.Model):
    """Individual chat message"""
    room = models.ForeignKey(
        ChatRoom,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chat_messages'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['room', '-created_at']),
            models.Index(fields=['sender', 'is_read']),
        ]
    
    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}"
    
    def mark_as_read(self):
        self.is_read = True
        self.save()
