from functools import wraps
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages


def role_required(*allowed_roles):
    """
    Decorator to require specific user role
    Usage: @role_required('OFFICER', 'ADMIN')
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, 'You do not have permission to access this page.')
                return redirect('dashboard-redirect')
        return _wrapped_view
    return decorator


def citizen_required(view_func):
    """Require CITIZEN role"""
    return role_required('CITIZEN')(view_func)


def officer_required(view_func):
    """Require OFFICER role"""
    return role_required('OFFICER')(view_func)


def dispatcher_required(view_func):
    """Require DISPATCHER role"""
    return role_required('DISPATCHER')(view_func)


def admin_required(view_func):
    """Require ADMIN role"""
    return role_required('ADMIN')(view_func)


def officer_or_dispatcher_required(view_func):
    """Require OFFICER or DISPATCHER role"""
    return role_required('OFFICER', 'DISPATCHER')(view_func)


def staff_required(view_func):
    """Require any staff role (OFFICER, DISPATCHER, ADMIN)"""
    return role_required('OFFICER', 'DISPATCHER', 'ADMIN')(view_func)
