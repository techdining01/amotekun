from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Dispatch
from .serializers import DispatchSerializer

User = get_user_model()


class DispatchViewSet(viewsets.ModelViewSet):
    queryset = Dispatch.objects.all()
    serializer_class = DispatchSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        """Set dispatcher on create"""
        serializer.save(assigned_dispatcher=self.request.user)
    
    @action(detail=True, methods=['post'])
    def transition(self, request, pk=None):
        """Transition dispatch to new status"""
        dispatch = self.get_object()
        new_status = request.data.get('status')
        
        if not new_status:
            return Response(
                {'error': 'status field is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            old_status, _ = dispatch.transition_to(new_status)
            serializer = self.get_serializer(dispatch)
            return Response({
                'message': f'Status changed from {old_status} to {new_status}',
                'dispatch': serializer.data
            })
        except ValueError as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def assign_officer(self, request, pk=None):
        """Assign an officer to this dispatch"""
        dispatch = self.get_object()
        officer_id = request.data.get('officer_id')
        
        if not officer_id:
            return Response(
                {'error': 'officer_id field is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            officer = User.objects.get(id=officer_id, role='OFFICER')
            dispatch.assign_officer(officer)
            serializer = self.get_serializer(dispatch)
            return Response({
                'message': f'Officer {officer.username} assigned',
                'dispatch': serializer.data
            })
        except User.DoesNotExist:
            return Response(
                {'error': 'Officer not found or invalid role'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except ValueError as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel this dispatch"""
        dispatch = self.get_object()
        reason = request.data.get('reason', '')
        
        try:
            old_status = dispatch.cancel(reason)
            serializer = self.get_serializer(dispatch)
            return Response({
                'message': f'Dispatch cancelled from {old_status}',
                'dispatch': serializer.data
            })
        except ValueError as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'])
    def my_assignments(self, request):
        """Get dispatches assigned to current officer"""
        if request.user.role != 'OFFICER':
            return Response(
                {'error': 'Only officers can view their assignments'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        dispatches = Dispatch.objects.filter(
            assigned_officer=request.user
        ).exclude(status__in=['resolved', 'cancelled'])
        
        serializer = self.get_serializer(dispatches, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_created(self, request):
        """Get dispatches created by current dispatcher"""
        if request.user.role != 'DISPATCHER':
            return Response(
                {'error': 'Only dispatchers can view their created dispatches'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        dispatches = Dispatch.objects.filter(
            assigned_dispatcher=request.user
        )
        
        serializer = self.get_serializer(dispatches, many=True)
        return Response(serializer.data)
