from django.contrib import admin
from .models import ChatRoom, ChatMessage


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'room_type', 'incident', 'dispatch', 'station', 'created_at']
    list_filter = ['room_type', 'created_at']
    search_fields = ['name']


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['room', 'sender', 'content_preview', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']
    search_fields = ['content', 'sender__username']
    readonly_fields = ['created_at']
    
    def content_preview(self, obj):
        return obj.content[:50]
    content_preview.short_description = 'Content'
