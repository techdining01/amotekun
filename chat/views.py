from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ChatRoom, ChatMessage
from .serializers import ChatRoomSerializer, ChatMessageSerializer


class ChatRoomViewSet(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save()
    
    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        """Get all messages for a room"""
        room = self.get_object()
        messages = room.messages.all()
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark all messages in room as read for current user"""
        room = self.get_object()
        room.messages.filter(sender=request.user).update(is_read=True)
        return Response({'status': 'messages marked as read'})


class ChatMessageViewSet(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_unread(self, request):
        """Get unread messages for current user"""
        messages = ChatMessage.objects.filter(
            room__in=ChatRoom.objects.filter(messages__sender=request.user),
            is_read=False
        ).exclude(sender=request.user)
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)
