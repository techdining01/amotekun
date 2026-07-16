from rest_framework.permissions import BasePermission


class IsPlatformAdmin(BasePermission):
    """
    Allows access only to platform administrators.
    """
    
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == "ADMIN")