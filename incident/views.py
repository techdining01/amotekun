from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def home(request):
    if request.user.is_authenticated:
        role_map = {
            'ADMIN': ('dashboards/admin.html', 'Admin'),
            'DISPATCHER': ('dashboards/dispatcher.html', 'Dispatcher'),
            'OFFICER': ('dashboards/officer.html', 'Officer'),
        }
        template, role_display = role_map.get(request.user.role, ('index.html', 'Citizen'))
        return render(request, template, {'role_display': role_display})
    return render(request, "index.html")
