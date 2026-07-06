from rest_framework.permissions import BasePermission
from dashboard.models import User


class IsCitizen(BasePermission):
    """Allows access only to citizens."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.ROLE_CHOICES[0][0]


class IsOfficer(BasePermission):
    """Allows access only to officers."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.ROLE_CHOICES[1][0]


class IsDispatcher(BasePermission):
    """Allows access only to dispatchers."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.ROLE_CHOICES[2][0]


class IsAdmin(BasePermission):
    """Allows access only to admins."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.ROLE_CHOICES[3][0]


class IsOfficerOrHigher(BasePermission):
    """Allows access to officers, dispatchers, and admins."""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role in [
            User.ROLE_CHOICES[1][0],
            User.ROLE_CHOICES[2][0],
            User.ROLE_CHOICES[3][0]
        ]


class IsDispatcherOrHigher(BasePermission):
    """Allows access to dispatchers and admins."""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role in [
            User.ROLE_CHOICES[2][0],
            User.ROLE_CHOICES[3][0]
        ]


class IsAdminOnly(BasePermission):
    """Allows access only to admins."""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role == User.ROLE_CHOICES[3][0]
