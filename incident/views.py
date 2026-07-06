from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def home(request):
    if request.user.is_authenticated:
        role_map = {
            'ADMIN': ('dashboard/admin_dashboard.html', 'Admin'),
            'DISPATCHER': ('dashboard/dispatcher_dashboard.html', 'Dispatcher'),
            'OFFICER': ('dashboard/officer_dashboard.html', 'Officer'),
            'CITIZEN': ('dashboard/citizen_dashboard.html', 'Citizen'),
        }
        template, role_display = role_map.get(request.user.role, ('index.html', 'Citizen'))
        return render(request, template, {'role_display': role_display})
    return render(request, "index.html")
