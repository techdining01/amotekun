from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def role_redirect(request):
    """
    Redirect user to their role-specific dashboard
    """
    user = request.user
    role = user.role
    
    role_urls = {
        'CITIZEN': 'citizen-dashboard',
        'OFFICER': 'officer-dashboard',
        'DISPATCHER': 'dispatcher-dashboard',
        'ADMIN': 'admin-dashboard',
    }
    
    dashboard_url = role_urls.get(role, 'citizen-dashboard')
    return redirect(dashboard_url)


@login_required
def dashboard_view(request):
    """
    Generic dashboard view - renders role-specific template
    """
    user = request.user
    role = user.role
    
    template_map = {
        'CITIZEN': 'dashboard/citizen_dashboard.html',
        'OFFICER': 'dashboard/officer_dashboard.html',
        'DISPATCHER': 'dashboard/dispatcher_dashboard.html',
        'ADMIN': 'dashboard/admin_dashboard.html',
    }
    
    template = template_map.get(role, 'dashboard/citizen_dashboard.html')
    
    context = {
        'user': user,
        'role': role,
        'role_display': user.get_role_display(),
    }
    
    return render(request, template, context)


