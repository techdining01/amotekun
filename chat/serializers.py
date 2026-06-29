from rest_framework import serializers
from .models import ChatRoom, ChatMessage


class ChatRoomSerializer(serializers.ModelSerializer):
    message_count = serializers.IntegerField(source='messages.count', read_only=True)
    last_message = serializers.SerializerMethodField()
    
    class Meta:
        model = ChatRoom
        fields = ['id', 'name', 'room_type', 'incident', 'dispatch', 'station', 
                  'created_at', 'message_count', 'last_message']
        read_only_fields = ['created_at']
    
    def get_last_message(self, obj):
        last = obj.messages.last()
        if last:
            return {
                'id': last.id,
                'sender': last.sender.username,
                'content': last.content,
                'created_at': last.created_at.isoformat()
            }
        return None


class ChatMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.username', read_only=True)
    room_name = serializers.CharField(source='room.name', read_only=True)
    
    class Meta:
        model = ChatMessage
        fields = ['id', 'room', 'sender', 'sender_name', 'content', 
                  'created_at', 'is_read', 'room_name']
        read_only_fields = ['created_at', 'is_read']
