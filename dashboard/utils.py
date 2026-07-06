from functools import wraps
from django.http import HttpResponseForbidden
from dashboard.models import User


def role_required(*roles):
    """Decorator to restrict view access to specific user roles."""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("You must be logged in to access this page.")
            if request.user.role not in roles:
                return HttpResponseForbidden("You do not have permission to access this page.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def citizen_required(view_func):
    """Decorator to restrict view access to citizens."""
    return role_required(User.ROLE_CHOICES[0][0])(view_func)


def officer_required(view_func):
    """Decorator to restrict view access to officers."""
    return role_required(User.ROLE_CHOICES[1][0])(view_func)


def dispatcher_required(view_func):
    """Decorator to restrict view access to dispatchers."""
    return role_required(User.ROLE_CHOICES[2][0])(view_func)


def admin_required(view_func):
    """Decorator to restrict view access to admins."""
    return role_required(User.ROLE_CHOICES[3][0])(view_func)


def officer_or_higher(view_func):
    """Decorator to restrict view access to officers, dispatchers, and admins."""
    return role_required(
        User.ROLE_CHOICES[1][0],
        User.ROLE_CHOICES[2][0],
        User.ROLE_CHOICES[3][0]
    )(view_func)


def dispatcher_or_higher(view_func):
    """Decorator to restrict view access to dispatchers and admins."""
    return role_required(
        User.ROLE_CHOICES[2][0],
        User.ROLE_CHOICES[3][0]
    )(view_func)
